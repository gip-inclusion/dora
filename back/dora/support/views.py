from django.db.models import (
    BooleanField,
    Case,
    Count,
    Exists,
    OuterRef,
    Prefetch,
    Q,
    Value,
    When,
)
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.exceptions import PermissionDenied

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.pagination import OptionalPageNumberPagination
from dora.core.utils import TRUTHY_VALUES
from dora.services.enums import ServiceStatus
from dora.services.models import Service
from dora.structures.models import Structure, StructureMember, StructurePutativeMember
from dora.support.serializers import (
    ServiceAdminListSerializer,
    ServiceAdminSerializer,
    StructureAdminListSerializer,
    StructureAdminSerializer,
)


class StructureAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in [*permissions.SAFE_METHODS, "PATCH"]:
            return (
                user
                and user.is_authenticated
                and (user.is_staff or (user.is_manager and user.departments))
            )
        return False


class ServiceAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in [*permissions.SAFE_METHODS, "PATCH"]:
            return user and user.is_authenticated and user.is_staff
        return False


class ModerationMixin:
    def perform_update(self, serializer):
        status_before_update = serializer.instance.moderation_status
        status_after_update = (
            ModerationStatus(serializer.validated_data.get("moderation_status"))
            or status_before_update
        )

        if not status_before_update != status_after_update:
            raise serializers.ValidationError(
                "Mise à jour du statut de modération sans changement de statut"
            )
        msg = "Statut de modération changé par un•e membre de l'équipe"
        send_moderation_notification(
            serializer.instance, self.request.user, msg, status_after_update
        )


class StructureAdminViewSet(
    ModerationMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = StructureAdminSerializer
    permission_classes = [StructureAdminPermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        user = self.request.user
        department = self.request.query_params.get("department")

        if department:
            if user.is_manager:
                # assuré par StructureAdminPermission
                assert user.departments
                if department not in user.departments:
                    raise PermissionDenied
            structures = Structure.objects.filter(department=department)
        else:
            if user.is_manager:
                structures = Structure.objects.filter(department__in=user.departments)
            elif user.is_staff:
                structures = Structure.objects.all()
            else:
                raise PermissionDenied

        moderation = self.request.query_params.get("moderation") in TRUTHY_VALUES
        if moderation:
            return structures.exclude(moderation_status=ModerationStatus.VALIDATED)

        # Base queryset with essential select_related only
        structures = structures.select_related(
            "parent", "creator", "last_editor", "source"
        )

        # Optimize prefetch_related with targeted querysets
        structures = structures.prefetch_related(
            Prefetch(
                "membership",
                queryset=StructureMember.objects.select_related("user").filter(
                    user__is_active=True
                ),
            ),
            Prefetch(
                "putative_membership",
                queryset=StructurePutativeMember.objects.select_related("user").filter(
                    user__is_active=True
                ),
            ),
            Prefetch(
                "services",
                queryset=Service.objects.select_related("last_editor")
                .prefetch_related("categories")
                .filter(~Q(status=ServiceStatus.ARCHIVED)),
            ),
            "branches",
        )

        # Split complex annotations into separate queries or simpler ones
        structures = structures.annotate(
            # Keep simple counts
            num_draft_services=Count(
                "services",
                filter=Q(services__status=ServiceStatus.DRAFT),
            ),
            num_published_services=Count(
                "services",
                filter=Q(services__status=ServiceStatus.PUBLISHED),
            ),
            num_active_services=Count(
                "services",
                filter=~Q(services__status=ServiceStatus.ARCHIVED),
            ),
            # Simplified boolean fields
            has_valid_admin=Exists(
                StructureMember.objects.filter(
                    structure=OuterRef("pk"),
                    is_admin=True,
                    user__is_valid=True,
                    user__is_active=True,
                )
            ),
            awaiting_moderation=Case(
                When(
                    moderation_status__in=[
                        ModerationStatus.NEED_NEW_MODERATION,
                        ModerationStatus.NEED_INITIAL_MODERATION,
                    ],
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )

        return structures

    def get_serializer_class(self):
        if self.action == "list":
            return StructureAdminListSerializer
        return super().get_serializer_class()


class ServiceAdminViewSet(
    ModerationMixin,
    mixins.RetrieveModelMixin,
    mixins.UpdateModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = ServiceAdminSerializer
    permission_classes = [ServiceAdminPermission]
    pagination_class = OptionalPageNumberPagination

    lookup_field = "slug"

    def get_queryset(self):
        moderation = self.request.query_params.get("moderation") in TRUTHY_VALUES
        all_services = Service.objects.select_related("structure").filter(
            status=ServiceStatus.PUBLISHED
        )
        if moderation:
            return all_services.exclude(moderation_status=ModerationStatus.VALIDATED)
        return all_services

    def get_serializer_class(self):
        if self.action == "list":
            return ServiceAdminListSerializer
        return super().get_serializer_class()
