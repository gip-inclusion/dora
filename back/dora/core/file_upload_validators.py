import logging

import magic
from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import UploadedFile

logger = logging.getLogger(__name__)


def sanitize_for_log(value: str) -> str:
    if not isinstance(value, str):
        return value
    return value.replace("\r", "").replace("\n", "")


def validate_file_size(file_size: int, structure_id=None):
    if file_size > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        extra = {
            "reason": "FILE_TOO_BIG",
            "size": file_size,
            "max_allowed": settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024,
        }
        if structure_id is not None:
            extra["structure_id"] = structure_id
        logger.warning("file_upload_rejected", extra=extra)
        raise ValidationError("FILE_TOO_BIG")


def validate_file_extension(filename: str, structure_id=None):
    declared_extension = filename.rsplit(".", 1)[-1].lower()
    if declared_extension not in settings.ALLOWED_UPLOADED_FILES_EXTENSIONS:
        extra = {
            "reason": "INVALID_EXTENSION",
            "declared_extension": sanitize_for_log(declared_extension),
        }
        if structure_id is not None:
            extra["structure_id"] = structure_id
        logger.warning("file_upload_rejected", extra=extra)
        raise ValidationError("INVALID_EXTENSION")


def validate_file_content(filename: str, file_obj: UploadedFile, structure_id=None):
    buffer = file_obj.read(4096)

    file_obj.seek(0)

    detected_mime_type = magic.from_buffer(buffer, mime=True)

    declared_extension = filename.rsplit(".", 1)[-1].lower()
    allowed_extensions_for_mime = settings.ALLOWED_MIME_TYPES.get(
        detected_mime_type, []
    )

    if declared_extension not in allowed_extensions_for_mime:
        extra = {
            "reason": "MIME_MISMATCH",
            "declared_extension": sanitize_for_log(declared_extension),
            "detected_mime": detected_mime_type,
        }
        if structure_id is not None:
            extra["structure_id"] = structure_id
        logger.warning("file_upload_rejected", extra=extra)
        raise ValidationError("INVALID_FILE_CONTENT")


def validate_upload(filename: str, file_obj: UploadedFile, structure_id=None) -> None:
    validate_file_size(file_obj.size, structure_id)

    if len(filename) > settings.MAX_FILENAME_LENGTH:
        raise ValidationError("FILENAME_TOO_LONG")

    if "." not in filename:
        raise ValidationError("MISSING_EXTENSION")

    validate_file_extension(filename, structure_id)

    validate_file_content(filename, file_obj, structure_id)
