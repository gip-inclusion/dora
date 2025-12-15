import logging

import magic
from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.exceptions import PermissionDenied, ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from dora.services.models import Service
from dora.structures.models import Structure

logger = logging.getLogger(__name__)


def _validate_upload(filename: str, file_obj: UploadedFile, structure_id=None) -> None:
    if file_obj.size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        logger.warning(
            "file_upload_rejected",
            extra={
                "reason": "FILE_TOO_BIG",
                "size": file_obj.size,
                "max_allowed": settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024,
                "structure_id": structure_id,
            },
        )
        raise ValidationError("FILE_TOO_BIG")

    if len(filename) > settings.MAX_FILENAME_LENGTH:
        raise ValidationError("FILENAME_TOO_LONG")

    if "." not in filename:
        raise ValidationError("MISSING_EXTENSION")

    declared_extension = filename.rsplit(".", 1)[-1].lower()
    if declared_extension not in settings.ALLOWED_UPLOADED_FILES_EXTENSIONS:
        logger.warning(
            "file_upload_rejected",
            extra={
                "reason": "INVALID_EXTENSION",
                "structure_id": structure_id,
                "declared_extension": declared_extension,
            },
        )
        raise ValidationError("INVALID_EXTENSION")

    mime = magic.Magic(mime=True)
    detected_mime_type = mime.from_buffer(file_obj.read(2048))
    file_obj.seek(0)

    allowed_extensions_for_mime = settings.ALLOWED_MIME_TYPES.get(
        detected_mime_type, []
    )
    if declared_extension not in allowed_extensions_for_mime:
        logger.warning(
            "file_upload_rejected",
            extra={
                "reason": "MIME_MISMATCH",
                "structure_id": structure_id,
                "declared_extension": declared_extension,
                "detected_mime": detected_mime_type,
            },
        )
        raise ValidationError("INVALID_FILE_CONTENT")


@api_view(["POST"])
@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
def upload(request: Request, filename: str, structure_slug: str) -> Response:
    structure = get_object_or_404(Structure.objects.all(), slug=structure_slug)

    if not structure.can_edit_services(request.user):
        raise PermissionDenied(
            "Uniquement les membres et les gestionnaires territoires peuvent charger des documents."
        )

    file_obj = request.data["file"]
    _validate_upload(filename, file_obj, structure.id)
    clean_filename = (
        f"{settings.ENVIRONMENT}/{structure.pk}/{get_valid_filename(filename)}"
    )
    result = default_storage.save(clean_filename, file_obj)
    return Response({"key": result}, status=201)


@api_view(["POST"])
@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
def safe_upload(request: Request, filename: str) -> Response:
    file_obj = request.data["file"]
    _validate_upload(filename, file_obj)
    clean_filename = f"{settings.ENVIRONMENT}/#orientations/{get_random_string(32)}/{get_valid_filename(filename)}"
    result = default_storage.save(clean_filename, file_obj)
    return Response({"key": result}, status=201)


@api_view()
@permission_classes([permissions.AllowAny])
def ping(request: Request) -> Response:
    check_services = Service.objects.exists()
    if check_services:
        return Response("ok", status=200)
    return Response("ko", status=500)


def trigger_error(request: Request) -> None:
    division_by_zero = 1 / 0
    print(division_by_zero)
