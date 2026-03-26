from django.conf import settings
from django.db.models import Prefetch
from rest_framework import permissions, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.versioning import NamespaceVersioning

from dora.core.pagination import OptionalPageNumberPagination
from dora.decoupage_administratif.models import (
    EPCI,
    AdminDivisionType,
    City,
)
from dora.orientations.models import Orientation, OrientationStatus
from dora.services.models import Service
from dora.structures.models import DisabledDoraFormDIStructure

from .serializers import DisabledDoraFormDIStructureSerializer, ServiceSerializer

_ANSWERED_ORIENTATIONS_QUERYSET = Orientation.objects.filter(
    status__in=[OrientationStatus.ACCEPTED, OrientationStatus.REJECTED],
    processing_date__isnull=False,
).only("creation_date", "processing_date")

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
    Prefetch("orientations", queryset=_ANSWERED_ORIENTATIONS_QUERYSET),
]


class APIPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return settings.ENVIRONMENT == "local" or (
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

    def _warm_geo_caches(self, services):
        city_codes = [
            s.diffusion_zone_details
            for s in services
            if s.diffusion_zone_type == AdminDivisionType.CITY
        ]
        epci_codes = [
            s.diffusion_zone_details
            for s in services
            if s.diffusion_zone_type == AdminDivisionType.EPCI
        ]
        City.objects.warm_cache(city_codes)
        EPCI.objects.warm_cache(epci_codes)

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            self._warm_geo_caches(page)
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        self._warm_geo_caches(queryset)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DisabledDoraFormDIStructureViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = (APIPermission,)
    serializer_class = DisabledDoraFormDIStructureSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = OptionalPageNumberPagination
    queryset = DisabledDoraFormDIStructure.objects.all().order_by("pk")
