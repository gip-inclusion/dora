import logging

from django.conf import settings
from django.core.files.storage import default_storage
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename
from rest_framework import permissions
from rest_framework.decorators import (
    api_view,
    parser_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from dora.core.file_upload_validators import validate_upload
from dora.core.throttling import StructureUploadThrottle, UploadRateThrottle
from dora.services.models import Service
from dora.structures.models import Structure

logger = logging.getLogger(__name__)


@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
@throttle_classes([StructureUploadThrottle])
def upload(request: Request, filename: str, structure_slug: str) -> Response:
    structure = get_object_or_404(Structure.objects.all(), slug=structure_slug)

    if not structure.can_edit_services(request.user):
        raise PermissionDenied(
            "Uniquement les membres et les gestionnaires territoires peuvent charger des documents."
        )

    file_obj = request.data["file"]
    validate_upload(filename, file_obj, structure.id)
    clean_filename = (
        f"{settings.ENVIRONMENT}/{structure.pk}/{get_valid_filename(filename)}"
    )
    result = default_storage.save(clean_filename, file_obj)
    return Response({"key": result}, status=201)


@api_view(["POST"])
@parser_classes([MultiPartParser])
@permission_classes([IsAuthenticated])
@throttle_classes([UploadRateThrottle])
def safe_upload(request: Request, filename: str) -> Response:
    file_obj = request.data["file"]
    validate_upload(filename, file_obj)
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
