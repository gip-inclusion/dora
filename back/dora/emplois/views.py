from django.conf import settings
from django.db.models import CharField, Prefetch, Value
from rest_framework import mixins, permissions, viewsets
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.versioning import NamespaceVersioning

from dora.core.pagination import OptionalPageNumberPagination
from dora.orientations.models import Orientation
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    FundingLabel,
    Service,
)
from dora.structures.models import DisabledDoraFormDIStructure

from .serializers import (
    DisabledDoraFormDIStructureSerializer,
    EmploisOrientationSerializer,
    ReferenceDataSerializer,
    ServiceSerializer,
)

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
    Prefetch(
        "orientations",
        queryset=Orientation.objects.answered().only(
            "creation_date", "processing_date"
        ),
        to_attr="answered_orientations",
    ),
]


class APIPermission(permissions.BasePermission):
    allowed_methods = permissions.SAFE_METHODS

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.email == settings.EMPLOIS_EMAIL
            and request.method in self.allowed_methods
        )

    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view)


class ReferenceDataViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = (APIPermission,)
    serializer_class = ReferenceDataSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = OptionalPageNumberPagination

    def get_queryset(self):
        funding_label_qs = FundingLabel.objects.all().annotate(
            kind=Value("funding_label", output_field=CharField())
        )
        beneficiary_access_mode_qs = BeneficiaryAccessMode.objects.all().annotate(
            kind=Value("beneficiary_access_mode", output_field=CharField())
        )
        coach_orientation_mode_qs = CoachOrientationMode.objects.all().annotate(
            kind=Value("coach_orientation_mode", output_field=CharField())
        )

        return funding_label_qs.union(
            beneficiary_access_mode_qs, coach_orientation_mode_qs
        )


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

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class DisabledDoraFormDIStructureViewSet(viewsets.ReadOnlyModelViewSet):
    versioning_class = NamespaceVersioning
    permission_classes = (APIPermission,)
    serializer_class = DisabledDoraFormDIStructureSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = OptionalPageNumberPagination
    queryset = DisabledDoraFormDIStructure.objects.all().order_by("pk")


class OrientationAPIPermission(APIPermission):
    allowed_methods = ("POST",)


class OrientationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (OrientationAPIPermission,)
    serializer_class = EmploisOrientationSerializer
    renderer_classes = (JSONRenderer,)

    def perform_create(self, serializer):
        # Pas de prescripteur ni d'envoi d'email : Les Emplois est une source
        # de confiance, l'orientation reste OUVERTE en attente de traitement.
        serializer.save(prescriber=None, prescriber_structure=None)
