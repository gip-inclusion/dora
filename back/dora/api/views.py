from django.conf import settings
from django.db.models import Exists, OuterRef
from itoutils.django.nexus.token import decode_token
from rest_framework import permissions, viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.versioning import NamespaceVersioning

from dora.core.pagination import OptionalPageNumberPagination
from dora.services.models import (
    Service,
    ServiceStatus,
)
from dora.structures.models import Structure, StructureMember

from ..sirene.models import Establishment
from ..users.enums import DiscoveryMethod, MainActivity
from ..users.models import User
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
            Service.objects.filter_for_DI()
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


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def handle_emplois_orientation(request, service_slug):
    op_jwt = request.GET.get("op")

    login_url = f"{settings.FRONTEND_URL}/auth/connexion"

    try:
        orientation_data = decode_token(op_jwt)
    except ValueError:
        return Response({"toast_message": "Lien expiré", "next_url": login_url})

    prescriber_data = orientation_data.get("prescriber")
    prescriber_email = prescriber_data.get("email")

    user_has_dora_account = User.objects.filter(email=prescriber_email).exists()

    if request.user.is_authenticated and request.user.email != prescriber_email:
        return Response({"next_url": login_url})

    if not user_has_dora_account:
        User.objects.create_user(
            prescriber_email,
            is_valid=True,
            main_activity=MainActivity.ACCOMPAGNATEUR,
            discovery_method=DiscoveryMethod.EMPLOIS_DE_L_INCLUSION,
        )

    structure_siret = prescriber_data.get("organization").get("siret")
    is_siret_recognized = Establishment.objects.filter(siret=structure_siret).exists()

    if not is_siret_recognized:
        return Response(
            {
                "next_url": f"{settings.FRONTEND_URL}/auth/rattachement?siret={structure_siret}",
                "known_siret": False,
            }
        )

    if not Structure.objects.filter(siret=structure_siret).exists():
        return Response(
            {
                "known_siret": False,
                "next_url": f"{settings.FRONTEND_URL}/auth/rattachement?siret={structure_siret}",
                "user_is_admin": True,
            }
        )

    if not StructureMember.objects.filter(
        structure__siret=structure_siret, user=request.user
    ).exists():
        return Response(
            {
                "next_url": f"{settings.FRONTEND_URL}/auth/rattachement?siret={structure_siret}&op={op_jwt}",
                "known_siret": True,
                "user_is_admin": False,
            },
        )

    structure = Structure.objects.filter(siret=structure_siret).first()

    return Response(
        {
            "user_structure_slug": structure.slug,
            "next_url": f"{settings.FRONTEND_URL}/services/{service_slug}?orientation={op_jwt}",
        }
    )
