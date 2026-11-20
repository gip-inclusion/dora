import functools
import hmac
import logging

from django.core import signing
from django.core.exceptions import PermissionDenied
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
from django.db.models import Count, Exists, OuterRef, Q
from django.shortcuts import get_object_or_404
from rest_framework import mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import APIException, MethodNotAllowed, ValidationError
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from dora.core.throttling import OrientationsExportLinkThrottle
from dora.core.utils import TRUTHY_VALUES
from dora.emplois.api_client import EmploisApiClient, EmploisAPIException
from dora.services.utils import DORA_UID_PREFIX, get_emplois_service_uid

from ..core.emails import sanitize_user_input_injected_in_email
from ..services.models import Service
from ..structures.models import Structure
from .emails import (
    send_message_to_beneficiary,
    send_message_to_prescriber,
    send_orientation_accepted_emails,
    send_orientation_created_to_structure,
    send_orientation_rejected_emails,
)
from .export_link import EXPORT_TYPES, read_export_token, send_export_link
from .models import (
    EMPLOIS_ORIENTATION_Q,
    ContactRecipient,
    Orientation,
    OrientationStatus,
    RejectionReason,
    SentContactEmail,
)
from .serializers import (
    EmploisReceivedOrientationExportSerializer,
    OrientationSerializer,
    ReceivedOrientationExportSerializer,
    SentOrientationExportSerializer,
)

logger = logging.getLogger(__name__)


class ModeratedOrientationPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, orientation):
        return orientation.status not in [
            OrientationStatus.MODERATION_PENDING,
            OrientationStatus.MODERATION_REJECTED,
        ]


class OrientationPermission(permissions.BasePermission):
    def has_permission(self, request, view):
        match request.method:
            case "DELETE":
                return False
            case _:
                return True

    def has_object_permission(self, request, view, orientation):
        match request.method:
            case "GET" | "POST":
                if h := request.query_params.get("h"):
                    if not hmac.compare_digest(h, orientation.get_query_id_hash()):
                        return False
                    if orientation.query_expired:
                        return False
                    return True
                return False
            case _:
                return False


class OrientationViewSet(
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    serializer_class = OrientationSerializer
    permission_classes = [ModeratedOrientationPermission, OrientationPermission]
    lookup_field = "query_id"

    def get_queryset(self):
        return Orientation.objects.select_related("emplois_orientation_data")

    @action(
        detail=True,
        methods=["post"],
        url_path="validate",
    )
    def validate(self, request, query_id=None):
        orientation = self.get_object()
        prescriber_message = self.request.data.get("message")
        beneficiary_message = self.request.data.get("beneficiary_message")

        try:
            sanitized_prescriber_message = sanitize_user_input_injected_in_email(
                prescriber_message
            )
        except DjangoValidationError as error:
            raise ValidationError({"message": error.messages})

        try:
            sanitized_beneficiary_message = sanitize_user_input_injected_in_email(
                beneficiary_message
            )
        except DjangoValidationError as error:
            raise ValidationError({"beneficiary_message": error.messages})

        if orientation.service:
            # L'objet service et les durées n'existent pas dans le cas des services DI
            orientation.duration_weekly_hours = (
                orientation.service.duration_weekly_hours
            )
            orientation.duration_weeks = orientation.service.duration_weeks
            orientation.save(update_fields=["duration_weekly_hours", "duration_weeks"])
        orientation.set_status(OrientationStatus.ACCEPTED, request.user)

        send_orientation_accepted_emails(
            orientation, sanitized_prescriber_message, sanitized_beneficiary_message
        )
        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="reject",
    )
    def reject(self, request, query_id=None):
        orientation = self.get_object()
        message = self.request.data.get("message", "")
        reasons = self.request.data.get("reasons", [])

        try:
            sanitized_message = sanitize_user_input_injected_in_email(message)
        except DjangoValidationError as error:
            raise ValidationError({"message": error.messages})

        with transaction.atomic():
            orientation.delete_attachments()
            orientation.rejection_reasons.set(
                RejectionReason.objects.filter(value__in=reasons)
            )
            orientation.set_status(OrientationStatus.REJECTED, request.user)

            transaction.on_commit(
                functools.partial(
                    send_orientation_rejected_emails, orientation, sanitized_message
                )
            )

        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="contact/beneficiary",
    )
    def contact_beneficiary(self, request, query_id=None):
        orientation = self.get_object()
        if not orientation.beneficiary_email:
            raise ValidationError("Adresse email du bénéficiaire inconnue")
        message = self.request.data.get("message")
        cc_prescriber = self.request.data.get("cc_prescriber") in TRUTHY_VALUES
        cc_referent = self.request.data.get("cc_referent") in TRUTHY_VALUES

        sent_contact_emails = []
        cc = []

        if cc_prescriber:
            cc.append(orientation.prescriber_info.email)
            sent_contact_emails.append(ContactRecipient.PRESCRIBER)
        if (
            cc_referent
            and orientation.referent_email
            and orientation.referent_email != orientation.prescriber_info.email
        ):
            cc.append(orientation.referent_email)
            sent_contact_emails.append(ContactRecipient.REFERENT)

        send_message_to_beneficiary(orientation, message, cc)

        SentContactEmail.objects.create(
            orientation=orientation,
            recipient=ContactRecipient.BENEFICIARY,
            carbon_copies=sent_contact_emails,
        )
        return Response(status=204)

    @action(
        detail=True,
        methods=["post"],
        url_path="contact/prescriber",
    )
    def contact_prescriber(self, request, query_id=None):
        orientation = self.get_object()
        message = self.request.data.get("message")
        cc_beneficiary = self.request.data.get("cc_beneficiary") in TRUTHY_VALUES
        cc_referent = self.request.data.get("cc_referent") in TRUTHY_VALUES

        sent_contact_emails = []
        cc = []

        if cc_beneficiary and orientation.beneficiary_email:
            cc.append(orientation.beneficiary_email)
            sent_contact_emails.append(ContactRecipient.BENEFICIARY)
        if (
            cc_referent
            and orientation.referent_email
            and orientation.referent_email != orientation.prescriber_info.email
        ):
            cc.append(orientation.referent_email)
            sent_contact_emails.append(ContactRecipient.REFERENT)

        send_message_to_prescriber(orientation, message, cc)

        SentContactEmail.objects.create(
            orientation=orientation,
            recipient=ContactRecipient.PRESCRIBER,
            carbon_copies=sent_contact_emails,
        )

        return Response(status=204)

    @action(
        detail=True,
        methods=["patch"],
        url_path="refresh",
        permission_classes=[ModeratedOrientationPermission],
    )
    def refresh(self, request, query_id=None):
        # la régénération du hash est le seul point d'entrée "ouvert",
        # pas d'échange d'information, juste une demande traitée côté backend.
        orientation = self.get_object()
        orientation.refresh_query_expiration_date()

        # renvoi de l'e-mail avec un nouveau lien (uniquement pour la structure)
        send_orientation_created_to_structure(orientation)

        return Response(status=204)


def _emplois_service_names(emplois_orientations: list[dict]) -> dict[str, str]:
    """Résout le nom des services Dora référencés par Les Emplois.

    L'API renvoie un identifiant (``dora--<uuid>``) là où l'export attend un
    nom de service. Les identifiants d'autres sources sont ignorés.
    """
    service_ids = {
        uid.removeprefix(DORA_UID_PREFIX)
        for orientation in emplois_orientations
        if (uid := orientation.get("service_uid") or "").startswith(DORA_UID_PREFIX)
    }
    if not service_ids:
        return {}

    return {
        get_emplois_service_uid(service_id): name
        for service_id, name in Service.objects.filter(id__in=service_ids).values_list(
            "id", "name"
        )
    }


class ExportLinkExpired(APIException):
    status_code = 410
    default_detail = "Le lien de téléchargement a expiré."
    default_code = "export_link_expired"


class StructureOrientationsView(APIView):
    """Vue partagée pour les statistiques et l'export des orientations
    d'une structure.
    """

    permission_classes = [IsAuthenticated]

    # Renseigné via ``as_view(mode=...)`` pour distinguer les endpoints
    # qui partagent cette vue.
    mode: str | None = None

    def get_throttles(self):
        throttles = super().get_throttles()
        if self.mode == "export_link":
            throttles.append(OrientationsExportLinkThrottle())
        return throttles

    @staticmethod
    def sent_filter(structure: Structure) -> Q:
        return Q(prescriber_structure=structure)

    @staticmethod
    def received_filter(structure: Structure) -> Q:
        return (
            Q(service__structure=structure)
            & ~Q(
                status__in=[
                    OrientationStatus.MODERATION_PENDING,
                    OrientationStatus.MODERATION_REJECTED,
                ]
            )
            # Les orientations émises par Les Emplois sont déjà servies par
            # leur API : les compter ici aussi les doublonnerait.
            & ~EMPLOIS_ORIENTATION_Q
        )

    @classmethod
    def sent_orientations(cls, structure: Structure):
        return Orientation.objects.filter(cls.sent_filter(structure))

    @classmethod
    def received_orientations(cls, structure: Structure):
        return Orientation.objects.filter(cls.received_filter(structure))

    def _get_structure(self, structure_slug: str) -> Structure:
        structure = get_object_or_404(
            Structure.objects.annotate(
                has_services=Exists(Service.objects.filter(structure=OuterRef("pk")))
            ),
            slug=structure_slug,
        )

        if not structure.can_edit_services(self.request.user):
            raise PermissionDenied("L'utilisateur n'est pas membre de cette structure.")

        return structure

    def get(self, request: Request, structure_slug: str) -> Response:
        if self.mode == "export_link":
            raise MethodNotAllowed(request.method)

        structure = self._get_structure(structure_slug)

        if self.mode == "stats":
            return self._stats(structure)
        if self.mode == "export":
            return self._export(request, structure)

        raise RuntimeError(
            f"StructureOrientationsView appelée avec un mode inconnu : {self.mode!r}."
        )

    def post(self, request: Request, structure_slug: str) -> Response:
        if self.mode != "export_link":
            raise MethodNotAllowed(request.method)

        structure = self._get_structure(structure_slug)

        export_type = request.data.get("type")
        if export_type not in EXPORT_TYPES:
            raise ValidationError(
                {"type": "Le paramètre 'type' doit être 'sent' ou 'received'."}
            )

        send_export_link(request.user, structure, export_type)
        return Response(status=204)

    def _export_type_from_token(self, request: Request, structure: Structure) -> str:
        """Le téléchargement n'est possible qu'avec le lien reçu par e-mail :
        le jeton prouve que l'utilisateur a accès à sa boîte mail.
        """
        try:
            payload = read_export_token(request.query_params.get("token", ""))
        except signing.SignatureExpired:
            raise ExportLinkExpired()
        except signing.BadSignature:
            raise PermissionDenied("Lien de téléchargement invalide.")

        if (
            payload.get("user_id") != str(request.user.pk)
            or payload.get("structure_slug") != structure.slug
            or payload.get("type") not in EXPORT_TYPES
        ):
            raise PermissionDenied("Lien de téléchargement invalide.")

        return payload["type"]

    def _stats(self, structure: Structure) -> Response:
        sent_q = self.sent_filter(structure)
        received_q = self.received_filter(structure)
        pending_q = Q(status=OrientationStatus.PENDING)

        stats = Orientation.objects.filter(sent_q | received_q).aggregate(
            total_sent=Count("id", filter=sent_q),
            total_sent_pending=Count("id", filter=sent_q & pending_q),
            total_received=Count("id", filter=received_q),
            total_received_pending=Count("id", filter=received_q & pending_q),
        )
        try:
            emplois_counts = EmploisApiClient().get_received_orientations_count(
                structure_id=structure.id
            )
        except EmploisAPIException:
            # Les compteurs restent affichés avec les seules données Dora si
            # Les Emplois sont indisponibles (l'erreur est déjà loguée).
            emplois_counts = {"total_count": 0, "pending_count": 0}

        stats["total_received"] += emplois_counts["total_count"]
        stats["total_received_pending"] += emplois_counts["pending_count"]
        stats["structure_has_services"] = structure.has_services

        return Response(stats)

    def _export(self, request: Request, structure: Structure) -> Response:
        export_type = self._export_type_from_token(request, structure)

        if export_type == "sent":
            orientations = (
                self.sent_orientations(structure)
                .order_by("-creation_date")
                .select_related(
                    "service__structure",
                    "prescriber_structure",
                    "prescriber",
                    "emplois_orientation_data",
                )
            )
            return Response(
                SentOrientationExportSerializer(orientations, many=True).data
            )

        if export_type == "received":
            orientations = (
                self.received_orientations(structure)
                .order_by("-creation_date")
                .select_related(
                    "service__structure",
                    "prescriber_structure",
                    "prescriber",
                    "emplois_orientation_data",
                )
            )
            try:
                emplois_orientations = EmploisApiClient().fetch_received_orientations(
                    structure_id=structure.id
                )
            except EmploisAPIException:
                # L'export reste disponible avec les seules données Dora si
                # Les Emplois sont indisponibles (l'erreur est déjà loguée).
                emplois_orientations = []

            rows = ReceivedOrientationExportSerializer(orientations, many=True).data
            rows += EmploisReceivedOrientationExportSerializer(
                emplois_orientations,
                many=True,
                context={"service_names": _emplois_service_names(emplois_orientations)},
            ).data
            # ``creation_date`` est au format ``AAAA-MM-JJ`` : l'ordre
            # lexicographique correspond à l'ordre chronologique.
            rows.sort(key=lambda row: row["creation_date"], reverse=True)
            return Response(rows)

        raise RuntimeError(f"Type d'export inconnu : {export_type!r}.")
