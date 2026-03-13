from django.conf import settings
from rest_framework import permissions, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.versioning import NamespaceVersioning

from dora.core.pagination import OptionalPageNumberPagination
from dora.services.models import Service

from .serializers import ServiceSerializer

PREFETCH_RELATED_SERVICE_LIST = [
    "publics",
    "access_conditions",
    "requirements",
    "credentials",
    "funding_labels",
    "kinds",
    "coach_orientation_modes",
    "orientable_ft_services",
    "beneficiaries_access_modes",
]


class APIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.email == settings.EMPLOIS_EMAIL
            and request.method in permissions.SAFE_METHODS
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ServiceViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = (APIPermission,)
    serializer_class = ServiceSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = OptionalPageNumberPagination

    def get_queryset(self):
        return (
            Service.objects.filter_for_DI()
            .select_related("structure")
            .prefetch_related(*PREFETCH_RELATED_SERVICE_LIST)
            .order_by("pk")
        )
