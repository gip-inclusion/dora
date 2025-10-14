from datetime import timedelta
from operator import itemgetter
from urllib.parse import unquote

import requests
from django.conf import settings
from django.core.cache import cache
from django.db.models import Q
from django.http.response import Http404
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.utils.timezone import now
from furl import furl
from rest_framework import (
    exceptions,
    mixins,
    permissions,
    serializers,
    status,
    viewsets,
)
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

import dora.data_inclusion as data_inclusion
from dora.admin_express.models import City
from dora.admin_express.utils import arrdt_to_main_insee_code
from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.pagination import OptionalPageNumberPagination
from dora.core.utils import TRUTHY_VALUES
from dora.services.emails import send_service_feedback_email, send_service_sharing_email
from dora.services.enums import ServiceStatus
from dora.services.models import (
    AccessCondition,
    AdminDivisionType,
    BeneficiaryAccessMode,
    Bookmark,
    CoachOrientationMode,
    Credential,
    LocationKind,
    Public,
    Requirement,
    SavedSearch,
    Service,
    ServiceCategory,
    ServiceFee,
    ServiceKind,
    ServiceModel,
    ServiceModificationHistoryItem,
    ServiceStatusHistoryItem,
    ServiceSubCategory,
    UpdateFrequency,
)
from dora.services.utils import synchronize_service_from_model
from dora.stats.models import DeploymentLevel, DeploymentState
from dora.structures.models import Structure, StructureMember

from .serializers import (
    AnonymousServiceSerializer,
    BookmarkSerializer,
    FeedbackSerializer,
    SavedSearchSerializer,
    ServiceListSerializer,
    ServiceModelSerializer,
    ServiceSerializer,
)
from .utils import update_sync_checksum


class ServicePermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if request.method == "DELETE":
            return user and user.is_authenticated

        # Anybody can read
        if request.method in permissions.SAFE_METHODS:
            return True

        # Authentified user can read and write
        return user and user.is_authenticated

    def has_object_permission(self, request, view, service):
        user = request.user
        # Only suggestions can be deleted
        if (
            request.method == "DELETE"
            and not service.status == ServiceStatus.SUGGESTION
        ):
            return False

        # Anybody can read
        if request.method in permissions.SAFE_METHODS:
            return True

        return service.can_write(user)


def get_visible_services(user):
    all_services = (
        Service.objects.all()
        .select_related(
            "structure",
        )
        .prefetch_related(
            "kinds",
            "categories",
            "subcategories",
            "access_conditions",
            "publics",
            "beneficiaries_access_modes",
            "coach_orientation_modes",
            "requirements",
            "credentials",
            "location_kinds",
        )
    )

    # Everybody can see published services
    if not user or not user.is_authenticated:
        qs = all_services.filter(status=ServiceStatus.PUBLISHED)
    # Staff can see everything
    elif user.is_staff:
        qs = all_services
    elif user.is_manager and user.departments:
        qs = all_services.filter(
            Q(status=ServiceStatus.PUBLISHED)
            | Q(structure__department__in=user.departments)
            | Q(structure__membership__user=user)
        )
    else:
        # Authentified users can see everything in their structure
        # plus published services for other structures
        qs = all_services.filter(
            Q(status=ServiceStatus.PUBLISHED) | Q(structure__membership__user=user)
        )
    return qs.distinct()


class ServiceViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = [ServicePermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        structure_slug = self.request.query_params.get("structure")
        published_only = self.request.query_params.get("published") in TRUTHY_VALUES

        qs = get_visible_services(user)

        if structure_slug:
            qs = qs.filter(structure__slug=structure_slug)

        if published_only:
            qs = qs.filter(status=ServiceStatus.PUBLISHED)

        return qs.order_by("-modification_date")

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceListSerializer
        # We only want to expose the full ServiceSerializer if the user was
        # effectively validated:
        # - either they are staff
        # - either they have a validated email, and are members of a structure
        user = self.request.user
        if user.is_authenticated and (
            user.is_staff
            or (user.is_valid and StructureMember.objects.filter(user=user).exists())
        ):
            return ServiceSerializer
        return AnonymousServiceSerializer

    @action(
        detail=True,
        methods=["post"],
        url_path="feedback",
        permission_classes=[permissions.AllowAny],
    )
    def post_dora_service_feedback(self, request, slug):
        serializer = FeedbackSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        d = serializer.validated_data

        service = self.get_object()
        recipients = set()
        if service.last_editor:
            recipients.add(service.last_editor.email)
        recipients.update(admin.email for admin in service.structure.admins)

        send_service_feedback_email(
            service.name,
            service.get_absolute_url(),
            False,
            list(recipients),
            d["notify_support"],
            d["reasons"],
            d["name"],
            d["email"],
            d["details"],
        )

        return Response(status=201)

    @action(
        detail=True,
        methods=["post"],
        url_path="share",
        permission_classes=[permissions.AllowAny],
    )
    def share(self, request, slug):
        service = self.get_object()
        serialized_service = ServiceSerializer(
            service, context={"request": request}
        ).data
        return share_service(request, serialized_service, is_di=False)

    def perform_create(self, serializer):
        pub_date = None
        if serializer.validated_data.get("status") == ServiceStatus.PUBLISHED:
            pub_date = timezone.now()

        service = serializer.save(
            creator=self.request.user,
            last_editor=self.request.user,
            publication_date=pub_date,
            modification_date=timezone.now(),
        )

        if service.status == ServiceStatus.PUBLISHED:
            send_moderation_notification(
                service,
                self.request.user,
                "Service publié",
                ModerationStatus.NEED_INITIAL_MODERATION,
            )
        if service.model:
            service.last_sync_checksum = service.model.sync_checksum
            service.save()

    def _log_history(self, serializer, new_status=""):
        changed_fields = []
        for key, value in serializer.validated_data.items():
            original_value = getattr(serializer.instance, key)
            if type(original_value).__name__ == "ManyRelatedManager":
                original_value = set(original_value.all())
                has_changed = set(value) != original_value
            else:
                has_changed = value != original_value
            if has_changed:
                changed_fields.append(key)
        if changed_fields:
            ServiceModificationHistoryItem.objects.create(
                service=serializer.instance,
                user=self.request.user,
                fields=changed_fields,
                status=new_status,
            )
        return changed_fields

    def _update_status(self, service, new_status, previous_status, user):
        if new_status == ServiceStatus.PUBLISHED:
            service.publication_date = timezone.now()
            service.save()

        ServiceStatusHistoryItem.objects.create(
            service=service,
            user=user,
            new_status=new_status,
            previous_status=previous_status,
        )

    def perform_update(self, serializer):
        mark_synced = self.request.data.get("mark_synced", "") in TRUTHY_VALUES

        status_before_update = serializer.instance.status
        status_after_update = (
            serializer.validated_data.get("status") or status_before_update
        )

        # Historique de modifications
        changed_fields = self._log_history(serializer, status_after_update)

        # Synchronisation avec les modèles
        last_sync_checksum = serializer.instance.last_sync_checksum
        if mark_synced and serializer.instance.model:
            last_sync_checksum = serializer.instance.model.sync_checksum

        # Enregistrement des mises à jour
        service = serializer.save(
            last_editor=self.request.user,
            last_sync_checksum=last_sync_checksum,
            modification_date=timezone.now(),
        )

        # Historique des statuts
        if status_before_update != service.status:
            self._update_status(
                service, service.status, status_before_update, self.request.user
            )

        # Notifications
        newly_published = (
            status_before_update != service.status
            and service.status == ServiceStatus.PUBLISHED
        )
        if newly_published:
            send_moderation_notification(
                service,
                self.request.user,
                "Service publié",
                ModerationStatus.NEED_INITIAL_MODERATION,
            )
        elif changed_fields and service.status == ServiceStatus.PUBLISHED:
            send_moderation_notification(
                service,
                self.request.user,
                f"Service modifié ({' / '.join(changed_fields)})",
                ModerationStatus.NEED_NEW_MODERATION,
            )

    @action(
        detail=False,
        methods=["POST"],
        url_path="update-from-model",
        permission_classes=[permissions.IsAuthenticated],
    )
    def update_services_from_model(self, request):
        service_slugs = self.request.data.get("services")

        user = self.request.user
        services = Service.objects.filter(slug__in=service_slugs)

        # Vérification des permissions
        for service in services:
            if not service.can_write(user):
                raise PermissionDenied

        for service in services:
            synchronize_service_from_model(service, service.model)

            service.last_editor = self.request.user
            service.last_sync_checksum = service.model.sync_checksum
            service.modification_date = timezone.now()
            service.save()

        return Response(status=204)

    @action(
        detail=False,
        methods=["POST"],
        url_path="reject-update-from-model",
        permission_classes=[permissions.IsAuthenticated],
    )
    def reject_update_services_from_model(self, request):
        data = self.request.data.get("data")
        user = self.request.user

        for row in data:
            model_slug = row.get("model_slug", None)
            service_slug = row.get("service_slug", None)

            if model_slug and service_slug:
                service = Service.objects.filter(slug=service_slug).first()
                model = ServiceModel.objects.filter(slug=model_slug).first()

                if model and service and service.can_write(user):
                    service.last_sync_checksum = model.sync_checksum
                    service.save()

        return Response(status=204)

    @action(
        detail=False,
        methods=["POST"],
        url_path="mark-as-up-to-date",
        permission_classes=[permissions.IsAuthenticated],
    )
    def mark_services_as_up_to_date(self, request):
        service_slugs = self.request.data.get("services")

        user = self.request.user
        services = Service.objects.filter(slug__in=service_slugs)

        # Vérification des permissions
        for service in services:
            if not service.can_write(user):
                raise PermissionDenied

        for service in services:
            service.last_editor = self.request.user
            service.modification_date = timezone.now()
            service.save()

        return Response(status=204)


class BookmarkViewSet(
    viewsets.GenericViewSet,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BookmarkSerializer

    def get_queryset(self):
        user = self.request.user
        visible_and_active_services = get_visible_services(user).exclude(
            status=ServiceStatus.ARCHIVED
        )
        return Bookmark.objects.filter(
            Q(service__isnull=True) | Q(service__in=visible_and_active_services),
            user=user,
        ).order_by("-creation_date")

    def create(self, request):
        slug = request.data.get("slug")
        is_di = request.data.get("is_di")
        service = None
        if slug and not is_di:
            try:
                service = Service.objects.get(slug=slug)
            except Service.DoesNotExist:
                raise NotFound
        if service and not service.can_read(request.user):
            raise PermissionDenied

        bookmark, created = Bookmark.objects.get_or_create(
            user=self.request.user,
            service=service if not is_di else None,
            di_id=slug if is_di else "",
        )
        if not created:
            raise serializers.ValidationError("ce bookmark existe déjà")

        return Response(status=status.HTTP_201_CREATED)


class SavedSearchViewSet(
    mixins.CreateModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    mixins.DestroyModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = SavedSearchSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return SavedSearch.objects.filter(user=user).order_by("-creation_date")

    def get_serializer(self, *args, **kwargs):
        if self.action == "list":
            serializer_class = self.get_serializer_class()
            kwargs.setdefault("context", self.get_serializer_context())
            return serializer_class(with_new_services_count=True, *args, **kwargs)
        return super().get_serializer(*args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(
        detail=True,
        methods=["get"],
        url_path="recent",
        permission_classes=[permissions.AllowAny],
    )
    def get_recent_services(self, request, pk):
        saved_search = self.get_object()
        if saved_search.user != request.user:
            raise exceptions.PermissionDenied()
        results = saved_search.get_recent_services(
            (now() - timedelta(days=settings.RECENT_SERVICES_CUTOFF_DAYS)).date()
        )
        results.sort(key=itemgetter("publication_date"), reverse=True)
        return Response(results)


class ModelViewSet(ServiceViewSet):
    def get_serializer_class(self):
        return ServiceModelSerializer

    def get_queryset(self):
        structure_slug = self.request.query_params.get("structure")

        all_models = (
            ServiceModel.objects.all()
            .select_related(
                "structure",
            )
            .prefetch_related(
                "kinds",
                "categories",
                "subcategories",
                "access_conditions",
                "publics",
                "beneficiaries_access_modes",
                "coach_orientation_modes",
                "requirements",
                "credentials",
                "location_kinds",
            )
        )
        # Everybody can see models

        qs = all_models
        if structure_slug:
            qs = qs.filter(structure__slug=structure_slug)

        return qs.order_by("-modification_date").distinct()

    def perform_create(self, serializer):
        user = self.request.user
        service_slug = self.request.data.get("service")
        service = None
        # Création d'un modèle à partir d'un service
        if service_slug:
            try:
                service = Service.objects.get(slug=service_slug)
            except Service.DoesNotExist:
                raise Http404

            # On peut uniquement transformer en modèle un service
            # d'une de nos structures
            if not service.structure.can_edit_services(user):
                raise PermissionDenied

            if service.model:
                raise serializers.ValidationError(
                    "Impossible de copier un service synchronisé"
                )

        structure_slug = self.request.data.get("structure")
        try:
            structure = Structure.objects.get(slug=structure_slug)
        except Structure.DoesNotExist:
            raise Http404
        # On peut uniquement copier vers une structure dont on fait partie
        if not structure.can_edit_services(user):
            raise PermissionDenied

        model = serializer.save(
            creator=self.request.user,
            last_editor=self.request.user,
            is_model=True,
            modification_date=timezone.now(),
        )
        assert model.structure == structure

        # Doit être fait après la première sauvegarde pour prendre en compte
        # les champs M2M
        model.sync_checksum = update_sync_checksum(model)
        model.save()
        if service:
            service.model = model
            service.last_sync_checksum = model.sync_checksum
            service.save()

    def perform_update(self, serializer):
        changed_fields = self._log_history(serializer)
        model = serializer.save(
            last_editor=self.request.user,
            modification_date=timezone.now(),
        )

        model.sync_checksum = update_sync_checksum(model)
        model.save()

        if changed_fields:
            model.log_note(
                self.request.user,
                f"Modèle modifié ({' / '.join(changed_fields)})",
            )

            if self.request.data.get("update_all_services", "") in TRUTHY_VALUES:
                services = Service.objects.filter(model_id=model.id)

                for service in services:
                    synchronize_service_from_model(service, model)

                    service.log_note(
                        self.request.user,
                        f"Service modifié automatiquement suite à la mise à jour de son modèle ({' / '.join(changed_fields)})",
                    )

                    ServiceModificationHistoryItem.objects.create(
                        service=service,
                        user=self.request.user,
                        fields=changed_fields,
                        status=service.status,
                    )

                    service.last_editor = self.request.user
                    service.last_sync_checksum = model.sync_checksum
                    service.modification_date = timezone.now()

                    # On ne vérifie pas les droits sur les services liés au modèle,
                    # en partant du principe que s'il peut modifier le modèle
                    # alors il peut modifier les services liés
                    service.save()


@api_view()
@permission_classes([permissions.AllowAny])
def options(request):
    class CustomChoiceSerializer(serializers.ModelSerializer):
        value = serializers.IntegerField(source="id")
        label = serializers.CharField(source="name")
        structure = serializers.SlugRelatedField(slug_field="slug", read_only=True)

        class Meta:
            fields = ["value", "label", "structure"]

    class AccessConditionSerializer(CustomChoiceSerializer):
        class Meta(CustomChoiceSerializer.Meta):
            model = AccessCondition

    class PublicSerializer(CustomChoiceSerializer):
        class Meta(CustomChoiceSerializer.Meta):
            model = Public

    class RequirementSerializer(CustomChoiceSerializer):
        class Meta(CustomChoiceSerializer.Meta):
            model = Requirement

    class CredentialSerializer(CustomChoiceSerializer):
        class Meta(CustomChoiceSerializer.Meta):
            model = Credential

    class ServiceCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ServiceCategory
            fields = ["value", "label"]

    class ServiceSubCategorySerializer(serializers.ModelSerializer):
        class Meta:
            model = ServiceSubCategory
            fields = ["value", "label"]

    class ServiceKindSerializer(serializers.ModelSerializer):
        class Meta:
            model = ServiceKind
            fields = ["value", "label"]

    class BeneficiaryAccessModeSerializer(serializers.ModelSerializer):
        class Meta:
            model = BeneficiaryAccessMode
            fields = ["value", "label"]

    class CoachOrientationModeSerializer(serializers.ModelSerializer):
        class Meta:
            model = CoachOrientationMode
            fields = ["value", "label"]

    class LocationKindSerializer(serializers.ModelSerializer):
        class Meta:
            model = LocationKind
            fields = ["value", "label"]

    class ServiceFeeSerializer(serializers.ModelSerializer):
        class Meta:
            model = ServiceFee
            fields = ["value", "label"]

    def filter_custom_choices(choices):
        user = request.user
        if user.is_staff:
            return choices

        filters = Q(structure_id=None)

        if user.is_authenticated:
            user_structures = StructureMember.objects.filter(user=user).values_list(
                "structure_id", flat=True
            )
            filters |= Q(structure_id__in=user_structures)

            if user.is_manager and user.departments:
                manager_structures = Structure.objects.filter(
                    department__in=user.departments
                )
                filters |= Q(structure__in=manager_structures)

        return choices.filter(filters)

    user = request.user
    cache_key = "options:anon"

    # If options depend on user permissions, include user ID
    if user.is_authenticated:
        cache_key = f"options:user:{user.pk}"

    # Try to serve from cache
    cached_data = cache.get(cache_key)
    if cached_data is not None:
        return Response(cached_data)

    result = {
        "categories": ServiceCategorySerializer(
            ServiceCategory.objects.all(), many=True
        ).data,
        "subcategories": ServiceSubCategorySerializer(
            ServiceSubCategory.objects.all(), many=True
        ).data,
        "kinds": ServiceKindSerializer(
            ServiceKind.objects.all().order_by("label"), many=True
        ).data,
        "fee_conditions": ServiceFeeSerializer(
            ServiceFee.objects.all(), many=True
        ).data,
        "beneficiaries_access_modes": BeneficiaryAccessModeSerializer(
            BeneficiaryAccessMode.objects.all(), many=True
        ).data,
        "coach_orientation_modes": CoachOrientationModeSerializer(
            CoachOrientationMode.objects.all(), many=True
        ).data,
        "location_kinds": LocationKindSerializer(
            LocationKind.objects.all(), many=True
        ).data,
        "access_conditions": AccessConditionSerializer(
            filter_custom_choices(
                AccessCondition.objects.select_related("structure").all()
            ),
            many=True,
            context={"request": request},
        ).data,
        "publics": PublicSerializer(
            filter_custom_choices(Public.objects.select_related("structure").all()),
            many=True,
            context={"request": request},
        ).data,
        "requirements": RequirementSerializer(
            filter_custom_choices(
                Requirement.objects.select_related("structure").all()
            ),
            many=True,
            context={"request": request},
        ).data,
        "credentials": CredentialSerializer(
            filter_custom_choices(Credential.objects.select_related("structure").all()),
            many=True,
            context={"request": request},
        ).data,
        "diffusion_zone_type": [
            {"value": c[0], "label": c[1]} for c in AdminDivisionType.choices
        ],
        "update_frequencies": [
            {"value": c[0], "label": c[1]} for c in UpdateFrequency.choices
        ],
        "deployment_departments": [
            s["department_code"]
            for s in DeploymentState.objects.filter(
                state__in=[DeploymentLevel.IN_PROGRESS, DeploymentLevel.FINALIZING]
            ).values()
        ],
    }

    cache.set(cache_key, result, timeout=3600)
    return Response(result)


@api_view()
@permission_classes([permissions.AllowAny])
def service_di(request, di_id: str):
    """Retrieve a single service from data.inclusion.

    The ``di_client`` acts as an entrypoint to the data.inclusion service repository.

    The output format matches the ServiceSerializer.
    """
    di_id = unquote(di_id)
    source_di, di_service_id = di_id.split("--")

    user_agent = request.META.get("HTTP_USER_AGENT")
    user_hash = request.META.get("HTTP_ANONYMOUS_USER_HASH")

    di_client = data_inclusion.di_client_factory()

    try:
        raw_service = di_client.retrieve_service(
            source=source_di,
            id=di_service_id,
            user_agent=user_agent,
            user_hash=user_hash,
        )
    except requests.ConnectionError:
        return Response(status=status.HTTP_502_BAD_GATEWAY)

    if raw_service is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(
        data_inclusion.map_service(raw_service, request.user.is_authenticated)
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def share_di_service(
    request,
    di_id: str,
):
    source_di, di_service_id = di_id.split("--")

    di_client = data_inclusion.di_client_factory()

    try:
        raw_service = di_client.retrieve_service(source=source_di, id=di_service_id)
    except requests.ConnectionError:
        return Response(status=status.HTTP_502_BAD_GATEWAY)

    if raw_service is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    serialized_service = data_inclusion.map_service(
        raw_service, request.user.is_authenticated
    )
    return share_service(request, serialized_service, is_di=True)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def post_di_service_feedback(request, di_id: str):
    # Vérification de la validité des données
    serializer = FeedbackSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data

    # Récupération et sérialisation du service DI
    source_di, di_service_id = di_id.split("--")
    di_client = data_inclusion.di_client_factory()
    try:
        raw_service = di_client.retrieve_service(source=source_di, id=di_service_id)
    except requests.ConnectionError:
        return Response(status=status.HTTP_502_BAD_GATEWAY)
    if raw_service is None:
        return Response(status=status.HTTP_404_NOT_FOUND)

    service_name = raw_service["nom"]
    service_url = furl(settings.FRONTEND_URL) / "services" / f"di--{di_id}"
    contact_email = raw_service["courriel"] or raw_service["structure"]["courriel"]

    send_service_feedback_email(
        service_name,
        service_url,
        True,
        [contact_email] if contact_email else [],
        d["notify_support"],
        d["reasons"],
        d["name"],
        d["email"],
        d["details"],
    )

    return Response(status=201)


@api_view()
@permission_classes([permissions.AllowAny])
def search(request):
    city_code = request.GET.get("city")
    categories = request.GET.get("cats")
    subcategories = request.GET.get("subs")
    kinds = request.GET.get("kinds")
    fees = request.GET.get("fees")
    locs = request.GET.get("locs")
    funding = request.GET.get("funding")
    lat = request.GET.get("lat")
    lon = request.GET.get("lon")
    # Recherche unifiée activée par défaut
    unified_search_enabled = request.GET.get("unifiedSearchEnabled") != "false"

    categories_list = categories.split(",") if categories is not None else None
    subcategories_list = subcategories.split(",") if subcategories is not None else None
    kinds_list = kinds.split(",") if kinds is not None else None
    fees_list = fees.split(",") if fees is not None else None
    locs_list = locs.split(",") if locs is not None else None
    funding_labels_list = funding.split(",") if funding is not None else None
    lat = float(lat) if lat else None
    lon = float(lon) if lon else None
    from .search import search_services

    city_code = arrdt_to_main_insee_code(city_code)
    city = get_object_or_404(City, pk=city_code)

    di_client = data_inclusion.di_client_factory()

    sorted_services, metadata = search_services(
        request=request,
        di_client=di_client,
        city_code=city_code,
        city=city,
        categories=categories_list,
        subcategories=subcategories_list,
        kinds=kinds_list,
        fees=fees_list,
        location_kinds=locs_list,
        funding_labels=funding_labels_list,
        lat=lat,
        lon=lon,
        unified_search_enabled=unified_search_enabled,
    )

    return Response(
        {
            "city_bounds": city.geom.extent,
            "funding_labels": metadata["funding_labels"],
            "services": sorted_services,
        }
    )


def share_service(request, service, is_di):
    class ShareSerializer(serializers.Serializer):
        sender_name = serializers.CharField(required=False)
        recipient_email = serializers.EmailField()
        recipient_kind = serializers.ChoiceField(
            choices=["beneficiary", "professional"]
        )

    serializer = ShareSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    d = serializer.validated_data
    if not d.get("sender_name") and not request.user.is_authenticated:
        raise serializers.ValidationError(
            "Le champ `sender_name` est requis pour les soumissions anonymes"
        )
    sender_name = (
        request.user.get_full_name()
        if request.user.is_authenticated
        else d["sender_name"]
    )
    send_service_sharing_email(
        service, sender_name, d["recipient_email"], d["recipient_kind"], is_di
    )
    return Response(status=201)
