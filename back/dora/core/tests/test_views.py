from unittest.mock import patch

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import make_structure, make_user
from dora.structures.models import StructureMember


class StructureFileUploadTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()
        self.user = make_user(is_active=True)
        baker.make(StructureMember, user=self.user, structure=self.structure)
        self.url = f"/upload/{self.structure.slug}/test.pdf/"

        self.client.force_authenticate(user=self.user)

        self.file_mock = SimpleUploadedFile("test.pdf", b"content")

    @patch("dora.core.views.default_storage.save", return_value="upload_key")
    def test_structure_file_upload(self, mock_save):
        response = self.client.post(self.url, {"file": self.file_mock})

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(
            mock_save.call_args[0][0], f"local/{self.structure.pk}/test.pdf"
        )
        self.assertEqual(mock_save.call_args[0][1].name, self.file_mock.name)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["key"], "upload_key")

    def test_non_structure_members_cannot_upload_documents(self):
        non_member_user = make_user(is_active=True)

        self.client.force_authenticate(user=non_member_user)

        response = self.client.post(self.url, {"file": self.file_mock})

        self.assertEqual(response.status_code, 403)
        self.assertEqual(
            str(response.data["detail"]["message"]),
            "Uniquement les membres et les gestionnaires territoires peuvent charger des documents.",
        )

    @patch("dora.core.views.default_storage.save", return_value="upload_key")
    def test_department_managers_can_upload_documents(self, mock_save):
        department_manager = make_user(
            is_active=True, is_manager=True, departments=[self.structure.department]
        )

        self.client.force_authenticate(user=department_manager)

        response = self.client.post(self.url, {"file": self.file_mock})

        self.assertEqual(response.status_code, 201)

    def test_validate_file_name_with_url(self):
        response = self.client.post(
            f"/upload/{self.structure.slug}/invalid.txt/", {"file": self.file_mock}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data[0]["message"]),
            "INVALID_EXTENSION",
        )

    def test_validate_file_size(self):
        large_content = b"x" * (settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 + 1)
        large_file = SimpleUploadedFile("test.pdf", large_content)

        response = self.client.post(self.url, {"file": large_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data[0]["message"]),
            "FILE_TOO_BIG",
        )


class SafeFileUploadTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()
        self.user = make_user(is_active=True)
        baker.make(StructureMember, user=self.user, structure=self.structure)
        self.url = "/safe-upload/test.pdf/"

        self.file_mock = SimpleUploadedFile("test.pdf", b"content")

        self.client.force_authenticate(user=self.user)

    @patch("dora.core.views.get_random_string", return_value="random_string")
    @patch("dora.core.views.default_storage.save", return_value="upload_key")
    def test_safe_file_upload(self, mock_save, mock_random_string):
        response = self.client.post(self.url, {"file": self.file_mock})

        self.assertEqual(mock_save.call_count, 1)
        self.assertEqual(
            mock_save.call_args[0][0], "local/#orientations/random_string/test.pdf"
        )
        self.assertEqual(mock_save.call_args[0][1].name, self.file_mock.name)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["key"], "upload_key")

    def test_validate_file_name_with_url(self):
        response = self.client.post(
            "/safe-upload/invalid.txt/", {"file": self.file_mock}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data[0]["message"]),
            "INVALID_EXTENSION",
        )

    def test_file_name_contains_point(self):
        response = self.client.post(
            "/safe-upload/pdf/", {"file": SimpleUploadedFile("pdf", b"content")}
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data[0]["message"]),
            "INVALID_EXTENSION",
        )

    def test_validate_file_size(self):
        large_content = b"x" * (settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024 + 1)
        large_file = SimpleUploadedFile("test.pdf", large_content)

        response = self.client.post(self.url, {"file": large_file})

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data[0]["message"]),
            "FILE_TOO_BIG",
        )
