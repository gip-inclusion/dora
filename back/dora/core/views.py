import logging

from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename
from rest_framework import permissions
from rest_framework.decorators import api_view, parser_classes, permission_classes
from rest_framework.exceptions import ValidationError
from rest_framework.parsers import FileUploadParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from dora.services.models import Service
from dora.structures.models import Structure, StructureMember

logger = logging.getLogger(__name__)


def _validate_upload(file_name: str, file_size: int) -> None:
    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise ValidationError("FILE_TOO_BIG")
    if file_name.split(".")[-1] not in settings.ALLOWED_UPLOADED_FILES_EXTENSIONS:
        raise ValidationError("INVALID_EXTENSION")


@api_view(["POST"])
@parser_classes([FileUploadParser])
@permission_classes([IsAuthenticated])
def upload(request: Request, filename: str, structure_slug: str) -> Response:
    structure = get_object_or_404(Structure.objects.all(), slug=structure_slug)

    if not StructureMember.objects.filter(
        user=request.user,
        structure=structure,
        user__is_active=True,
        user__is_valid=True,
    ).exists():
        raise ValidationError(
            "Uniquement les membres actifs d'une structure peuvent charger des documents."
        )

    file_obj = request.data["file"]
    _validate_upload(filename, file_obj.size)
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
    _validate_upload(filename, file_obj.size)
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
