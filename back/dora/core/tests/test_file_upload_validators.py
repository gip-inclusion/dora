from unittest.mock import Mock, patch

import pytest
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from rest_framework.exceptions import ValidationError

from dora.core.file_upload_validators import (
    validate_file_content,
    validate_file_extension,
    validate_file_size,
    validate_upload,
)


@patch("dora.core.file_upload_validators.magic")
class ValidateUploadTestCase(TestCase):
    def test_does_not_raise_when_valid_upload(self, mock_magic_bytes):
        mock_magic_bytes.from_buffer.return_value = "application/pdf"

        file_obj = SimpleUploadedFile("test.pdf", b"content")
        validate_upload("test.pdf", file_obj)  # Should not raise

    def test_raise_when_filename_too_long(self, mock_magic_bytes):
        long_filename = "a" * (settings.MAX_FILENAME_LENGTH + 1) + ".pdf"
        file_obj = SimpleUploadedFile(long_filename, b"content")
        with self.assertRaises(ValidationError) as cm:
            validate_upload(long_filename, file_obj)
        self.assertEqual(str(cm.exception.detail[0]), "FILENAME_TOO_LONG")

    def test_raise_when_missing_extension(self, mock_magic_bytes):
        file_obj = SimpleUploadedFile("testfile", b"content")
        with self.assertRaises(ValidationError) as cm:
            validate_upload("testfile", file_obj)
        self.assertEqual(str(cm.exception.detail[0]), "MISSING_EXTENSION")

    def test_raise_when_file_too_large(self, mock_magic_bytes):
        file_size = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 + 1
        with self.assertRaises(ValidationError) as cm:
            validate_file_size(file_size)
        self.assertEqual(str(cm.exception.detail[0]), "FILE_TOO_BIG")

    def test_raise_when_invalid_file_content(self, mock_magic_bytes):
        mock_magic_instance = Mock()
        mock_magic_instance.from_buffer.return_value = "text/plain"
        mock_magic_bytes.return_value = mock_magic_instance

        file_obj = SimpleUploadedFile("test.pdf", b"content")
        with self.assertRaises(ValidationError) as cm:
            validate_file_content("test.pdf", file_obj)
        self.assertEqual(str(cm.exception.detail[0]), "INVALID_FILE_CONTENT")

    def test_raise_when_invalid_extension(self, mock_magic_bytes):
        with self.assertRaises(ValidationError) as cm:
            validate_file_extension("test.exe")
        self.assertEqual(str(cm.exception.detail[0]), "INVALID_EXTENSION")


# En-tête d’un conteneur OLE2 (.doc, .xls) : sur un buffer tronqué, libmagic
# ne peut pas lire la structure interne et renvoie un type générique.
OLE2_HEADER = bytes.fromhex("D0CF11E0A1B11AE1") + bytes(2040)


@pytest.mark.parametrize("filename", ["test.doc", "test.xls"])
def test_accepts_ole2_container_for_legacy_office_extensions(filename):
    file_obj = SimpleUploadedFile(filename, OLE2_HEADER)
    validate_file_content(filename, file_obj)  # ne doit pas lever d’exception


def test_rejects_ole2_container_with_unrelated_extension():
    file_obj = SimpleUploadedFile("test.pdf", OLE2_HEADER)
    with pytest.raises(ValidationError) as exc_info:
        validate_file_content("test.pdf", file_obj)
    assert str(exc_info.value.detail[0]) == "INVALID_FILE_CONTENT"
