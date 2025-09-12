from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models import BooleanField, Case, Count, Exists, OuterRef, Q, Value, When
from rest_framework import mixins, permissions, serializers, viewsets
from rest_framework.exceptions import PermissionDenied

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.core.pagination import OptionalPageNumberPagination
from dora.core.utils import TRUTHY_VALUES
from dora.services.enums import ServiceStatus
from dora.services.models import Service
from dora.structures.models import Structure, StructureMember
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

        structures = (
            structures.select_related("parent", "creator", "last_editor", "source")
            .prefetch_related(
                "membership__user",
                "putative_membership__user",
                "services__categories",
                "branches",
            )
            .annotate(
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
                has_valid_admin=Exists(
                    StructureMember.objects.filter(
                        structure=OuterRef("pk"),
                        is_admin=True,
                        user__is_valid=True,
                        user__is_active=True,
                    )
                ),
                is_orphan=Case(
                    When(
                        Q(membership__isnull=True)
                        & Q(putative_membership__isnull=True),
                        then=Value(True),
                    ),
                    default=Value(False),
                    output_field=BooleanField(),
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
                num_potential_members_to_validate=Count(
                    "putative_membership",
                    filter=Q(
                        putative_membership__invited_by_admin=False,
                        putative_membership__user__is_valid=True,
                        putative_membership__user__is_active=True,
                    ),
                ),
                num_potential_members_to_remind=Count(
                    "putative_membership",
                    filter=Q(
                        putative_membership__invited_by_admin=True,
                        putative_membership__user__is_active=True,
                    ),
                ),
                categories_list=ArrayAgg(
                    "services__categories__value",
                    distinct=True,
                    filter=Q(services__categories__isnull=False),
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
