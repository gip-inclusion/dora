from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import BooleanField, Case, Count, Exists, OuterRef, Q, Value, When
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response

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
    StructureAdminExportDataSerializer,
    StructureAdminListSerializer,
    StructureAdminSerializer,
)


class StructureAdminPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if request.method in [*permissions.SAFE_METHODS, "PATCH", "POST"]:
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

        structures = Structure.objects.all().annotate(
            num_draft_services=Count(
                "services",
                distinct=True,
                filter=Q(services__status=ServiceStatus.DRAFT),
            ),
            num_published_services=Count(
                "services",
                distinct=True,
                filter=Q(services__status=ServiceStatus.PUBLISHED),
            ),
            num_active_services=Count(
                "services",
                distinct=True,
                filter=~Q(services__status=ServiceStatus.ARCHIVED),
            ),
            is_orphan=Case(
                When(
                    Exists(StructureMember.objects.filter(structure=OuterRef("pk")))
                    | Exists(
                        StructurePutativeMember.objects.filter(structure=OuterRef("pk"))
                    ),
                    then=Value(False),
                ),
                default=Value(True),
                output_field=BooleanField(),
            ),
            is_waiting=Exists(
                StructurePutativeMember.objects.filter(
                    structure=OuterRef("pk"),
                    is_admin=True,
                    invited_by_admin=True,
                    user__is_active=True,
                ).exclude(
                    structure__membership__is_admin=True,
                    structure__membership__user__is_valid=True,
                    structure__membership__user__is_active=True,
                )
            ),
            num_outdated_services=Count(
                "services",
                distinct=True,
                filter=Service.objects.get_update_advised_filter("services__"),
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
            categories_list=ArrayAgg(
                "services__categories__value",
                distinct=True,
                filter=Q(services__categories__isnull=False),
            ),
        )

        if not self.action == "list":
            structures = structures.select_related(
                "parent", "creator", "last_editor", "source"
            )

        if department:
            if user.is_manager:
                # assuré par StructureAdminPermission
                assert user.departments
                if department not in user.departments:
                    raise PermissionDenied
            structures = structures.filter(department=department)
        else:
            if user.is_manager:
                structures = structures.filter(department__in=user.departments)

        moderation = self.request.query_params.get("moderation") in TRUTHY_VALUES
        if moderation:
            return structures.exclude(moderation_status=ModerationStatus.VALIDATED)

        return structures

    def get_serializer_class(self):
        if self.action == "list":
            return StructureAdminListSerializer
        return super().get_serializer_class()

    @action(detail=False, methods=["post"], url_path="export-data")
    def export_data(self, request):
        """
        Si un gestionnaire territoire a besoin d'un export des donées, cette route supplémente
        les infos fournies par StructureAdminListSerializer. La route a besoin d'être un POST
        parce que si on envoie beaucoup de structure slugs pour l'export et il faut le
        faire dans le body de la requête.
        """
        slugs = request.data.get("slugs", [])

        structures = Structure.objects.filter(slug__in=slugs).annotate(
            num_potential_members_to_validate=Count(
                "putative_membership",
                filter=Q(
                    putative_membership__invited_by_admin=False,
                    putative_membership__user__is_valid=True,
                    putative_membership__user__is_active=True,
                ),
                distinct=True,
            ),
            num_potential_members_to_remind=Count(
                "putative_membership",
                filter=Q(
                    putative_membership__invited_by_admin=True,
                    putative_membership__user__is_active=True,
                ),
                distinct=True,
            ),
            admin_emails=ArrayAgg(
                "membership__user__email",
                distinct=True,
                filter=Q(
                    membership__is_admin=True,
                    membership__user__is_valid=True,
                    membership__user__is_active=True,
                ),
            ),
            editor_emails=ArrayAgg(
                "services__last_editor__email",
                distinct=True,
                filter=Q(
                    ~Q(services__last_editor__email=settings.DORA_BOT_USER),
                    services__status=ServiceStatus.PUBLISHED,
                    services__last_editor__isnull=False,
                ),
            ),
            has_valid_admin=Exists(
                StructureMember.objects.filter(
                    structure=OuterRef("pk"),
                    is_admin=True,
                    user__is_valid=True,
                    user__is_active=True,
                )
            ),
            putative_admin_emails=ArrayAgg(
                "putative_membership__user__email",
                distinct=True,
                filter=Q(
                    putative_membership__is_admin=True,
                    putative_membership__invited_by_admin=True,
                    putative_membership__user__is_active=True,
                ),
            ),
        )

        serializer = StructureAdminExportDataSerializer(structures, many=True)
        return Response(serializer.data)


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
