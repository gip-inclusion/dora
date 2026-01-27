from django.conf import settings
from django.db.models import Exists, OuterRef
from django.utils import timezone
from rest_framework import permissions, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.versioning import NamespaceVersioning

from dora.core.pagination import OptionalPageNumberPagination
from dora.services.models import (
    Service,
    ServiceStatus,
)
from dora.structures.models import Structure, StructureMember

from .serializers import (
    ServiceSerializer,
    StructureSerializer,
)

############
# V2
############


class APIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.email == settings.DATA_INCLUSION_EMAIL
            and request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, service):
        user = request.user
        return (
            user.is_authenticated
            and user.email == settings.DATA_INCLUSION_EMAIL
            and request.method in permissions.SAFE_METHODS
        )


class StructureViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = [APIPermission]
    serializer_class = StructureSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = OptionalPageNumberPagination

    def get_queryset(self):
        structures = (
            Structure.objects.select_related("source")
            .prefetch_related("national_labels")
            .filter(is_obsolete=False)
        )

        has_published_service = Exists(
            Service.objects.filter(
                structure=OuterRef("pk"),
                status=ServiceStatus.PUBLISHED,
            )
        )
        has_member = Exists(
            StructureMember.objects.filter(
                structure=OuterRef("pk"),
            )
        )

        structures = structures.filter(has_published_service | has_member)

        return structures.order_by("pk")


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = [APIPermission]
    serializer_class = ServiceSerializer
    renderer_classes = [JSONRenderer]
    pagination_class = OptionalPageNumberPagination

    def get_queryset(self):
        return (
            Service.objects.published()
            .exclude(structure__is_obsolete=True)
            .exclude(structure__in=Structure.objects.orphans())
            .exclude(suspension_date__lt=timezone.localdate())
            .select_related("structure", "fee_condition", "source")
            .prefetch_related(
                "subcategories",
                "kinds",
                "location_kinds",
                "coach_orientation_modes",
                "beneficiaries_access_modes",
                "publics",
                "requirements",
                "credentials",
            )
            .order_by("pk")
        )
