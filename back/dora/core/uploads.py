import re

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


# Correspond aux préfixes des documents pour les orientations (#orientations/) ou les formulaires des services (structure UUID/).
MANAGED_KEY = re.compile(
    rf"^{re.escape(settings.ENVIRONMENT)}/"
    r"(#orientations/|[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}/)"
)


def iter_managed_objects():
    """Chercher le file path et la date de la dernière modification de tous les objets dans le bucket s3"""
    client = default_storage.connection.meta.client
    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(
        Bucket=settings.AWS_STORAGE_BUCKET_NAME,
        Prefix=f"{settings.ENVIRONMENT}/",
    ):
        for obj in page.get("Contents", ()):
            key = obj["Key"]
            if MANAGED_KEY.match(key):
                yield key, obj["LastModified"]
