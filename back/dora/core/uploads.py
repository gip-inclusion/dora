from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename

from dora.core.file_upload_validators import validate_upload


def save_orientation_attachment(filename: str, file_obj: UploadedFile) -> str:
    validate_upload(filename, file_obj)
    path = (
        f"{settings.ENVIRONMENT}/#orientations/"
        f"{get_random_string(32)}/{get_valid_filename(filename)}"
    )
    return default_storage.save(path, file_obj)
