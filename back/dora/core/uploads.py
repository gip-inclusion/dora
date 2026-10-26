from django.conf import settings
from django.core.files.storage import default_storage
from django.core.files.uploadedfile import UploadedFile
from django.utils.crypto import get_random_string
from django.utils.text import get_valid_filename

from dora.core.file_upload_validators import validate_upload


def _save_document(
    filename: str, file_obj: UploadedFile, prefix: str, structure_id=None
) -> str:
    validate_upload(filename, file_obj, structure_id)
    # Le segment aléatoire isole chaque document : sans lui, deux envois d'un fichier de
    # même nom sous le même préfixe produiraient la même clé S3, et le second écraserait
    # silencieusement le premier.
    path = (
        f"{settings.ENVIRONMENT}/{prefix}/"
        f"{get_random_string(32)}/{get_valid_filename(filename)}"
    )
    return default_storage.save(path, file_obj)


def save_orientation_attachment(filename: str, file_obj: UploadedFile) -> str:
    return _save_document(filename, file_obj, "#orientations")


def save_structure_document(filename: str, file_obj: UploadedFile, structure_id) -> str:
    return _save_document(
        filename, file_obj, str(structure_id), structure_id=structure_id
    )
