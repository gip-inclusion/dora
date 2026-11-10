import json
import logging

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import transaction
from django.db.models.functions import Coalesce
from django.utils import timezone
from rest_framework import generics, mixins, permissions, status, viewsets
from rest_framework.decorators import api_view, permission_classes, renderer_classes
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from dora.core.pagination import DefaultPageNumberPagination
from dora.core.throttling import UploadRateThrottle
from dora.core.uploads import save_orientation_attachment
from dora.orientations.emails import send_orientation_created_emails
from dora.orientations.models import Orientation
from dora.services.utils import get_emplois_service_uid

from .serializers import (
    DoraServiceMobilisationSerializer,
    DoraStructureViewSerializer,
    EmploisOrientationCreateSerializer,
    EmploisOrientationStatusSerializer,
    ExternalServiceMobilisationSerializer,
)

logger = logging.getLogger(__name__)

MAX_ORIENTATION_ATTACHMENTS = 20  # we have a few cases with ~10 files


class APIPermission(permissions.BasePermission):
    allowed_methods = permissions.SAFE_METHODS

    def has_permission(self, request, view):
        user = request.user
        return (
            user.is_authenticated
            and user.email == settings.EMPLOIS_EMAIL
            and request.method in self.allowed_methods
        )


class OrientationAPIPermission(APIPermission):
    allowed_methods = ("POST",)


class OrientationViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    permission_classes = (OrientationAPIPermission,)
    serializer_class = EmploisOrientationCreateSerializer
    parser_classes = (MultiPartParser, FormParser)
    renderer_classes = (JSONRenderer,)
    throttle_classes = (UploadRateThrottle,)

    def create(self, request, *args, **kwargs):
        try:
            payload = json.loads(request.data["data"])
        except (LookupError, TypeError, ValueError):
            raise ValidationError({"data": "Invalid or missing 'data' field."})

        serializer = self.get_serializer(data=payload)
        serializer.is_valid(raise_exception=True)

        attachments = request.FILES.getlist("attachments")
        if len(attachments) > MAX_ORIENTATION_ATTACHMENTS:
            raise ValidationError(
                {
                    "attachments": f"Vous ne pouvez pas joindre plus de {MAX_ORIENTATION_ATTACHMENTS} fichiers."
                }
            )

        saved_paths = []
        try:
            for file_obj in attachments:
                saved_paths.append(save_orientation_attachment(file_obj.name, file_obj))

            serializer.validated_data["beneficiary_attachments"] = saved_paths
            orientation = self.perform_create(serializer)
        except Exception:  # we want to delete files if any error occurs
            for path in saved_paths:
                default_storage.delete(path)
            raise

        response_data = dict(
            **serializer.initial_data,
            emplois_sync_uid=orientation.emplois_orientation_data.emplois_sync_uid,
        )
        if saved_paths:
            response_data["beneficiary_attachments"] = saved_paths
        return Response(response_data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        with transaction.atomic():
            orientation = serializer.save(
                prescriber=None,
                prescriber_structure=None,
            )
            send_orientation_created_emails(orientation)
            emplois_data = orientation.emplois_orientation_data
            transaction.on_commit(
                lambda: logger.info(
                    "emplois_orientation_created",
                    extra={
                        "emplois_sync_uid": str(emplois_data.emplois_sync_uid),
                        "orientation_id": str(orientation.id),
                        "beneficiary_id": str(emplois_data.beneficiary_id),
                        "structure_id": str(emplois_data.structure_id),
                        "prescriber_id": str(emplois_data.prescriber_id)
                        if emplois_data.prescriber_id
                        else None,
                        "service_id": get_emplois_service_uid(orientation.service_id)
                        if orientation.service_id
                        else orientation.di_service_id,
                    },
                )
            )
        return orientation


class AwareDateTimeField(DateTimeField):
    default_error_messages = {
        **DateTimeField.default_error_messages,
        "naive": "La date et l'heure doivent inclure une indication de fuseau horaire.",
    }

    def enforce_timezone(self, value):
        if timezone.is_naive(value):
            self.fail("naive")
        return super().enforce_timezone(value)


class OrientationStatusListView(generics.ListAPIView):
    """Statuts des orientations émises par Les Emplois, pour leur synchronisation."""

    permission_classes = (APIPermission,)
    serializer_class = EmploisOrientationStatusSerializer
    renderer_classes = (JSONRenderer,)
    pagination_class = DefaultPageNumberPagination

    def get_queryset(self):
        return (
            Orientation.objects.emplois()
            .annotate(updated_at=Coalesce("processing_date", "creation_date"))
            .select_related("emplois_orientation_data")
            .only(
                "status",
                "processing_date",
                "creation_date",
                "emplois_orientation_data__emplois_sync_uid",
            )
            .order_by("pk")
        )

    def filter_queryset(self, queryset):
        queryset = super().filter_queryset(queryset)

        # `?updated_after=<ISO 8601 avec fuseau horaire>` : synchronisation
        # incrémentale des statuts. Format attendu :
        # `YYYY-MM-DDThh:mm[:ss[.uuuuuu]]Z` ou `...+HH:MM` / `...-HH:MM`
        # (ex. `2026-07-13T13:00:00Z`).
        # Borne incluse pour ne pas rater une mise à jour simultanée ;
        # Les Emplois dédoublonnent via `emplois_sync_uid`.
        updated_after = self.request.query_params.get("updated_after")
        if updated_after:
            try:
                value = AwareDateTimeField().run_validation(updated_after)
            except ValidationError as exc:
                raise ValidationError({"updated_after": exc.detail}) from exc
            queryset = queryset.filter(updated_at__gte=value)
        return queryset


@api_view(["POST"])
@permission_classes([OrientationAPIPermission])
@renderer_classes([JSONRenderer])
def record_mobilisation_event(request):
    source = request.data.get("source")
    if not source:
        raise ValidationError({"source": "Ce champ est obligatoire."})

    is_dora = source == "dora"
    has_service = bool(request.data.get("service_id"))

    if is_dora and has_service:
        serializer_class = DoraServiceMobilisationSerializer
    elif is_dora:
        serializer_class = DoraStructureViewSerializer
    elif has_service:
        serializer_class = ExternalServiceMobilisationSerializer
    else:
        # Structure hors Dora : rien à enregistrer.
        return Response(status=status.HTTP_204_NO_CONTENT)

    serializer = serializer_class(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)
