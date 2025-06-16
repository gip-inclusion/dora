from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.utils.safestring import mark_safe
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.services.admin import ServiceAdmin
from dora.services.models import Service


@patch("dora.services.admin.messages")
@patch("dora.services.admin.import_services")
class ImportServicesViewTestCase(APITestCase):
    def setUp(self):
        self.user = baker.make("users.User", is_valid=True)

        self.admin_site = AdminSite()
        self.service_admin = ServiceAdmin(Service, self.admin_site)

        self.factory = RequestFactory()

        self.post_request = self.factory.post(
            "/admin/services/service/import-services/"
        )
        self.post_request.user = self.user

        self.mock_success_result = {
            "created_count": 5,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [],
        }
        self.mock_error_result = {
            "created_count": 0,
            "errors": [
                "Ligne 2 : SIRET manquant.",
                "Ligne 3 : Structure introuvable.",
            ],
            "duplicated_services": [],
            "geo_data_missing_lines": [],
        }
        self.mock_warning_result = {
            "created_count": 3,
            "errors": [],
            "duplicated_services": ["Service A", "Service B"],
            "geo_data_missing_lines": [
                {"idx": 1, "address": "123 Main St", "city": "Paris"},
                {"idx": 3, "address": "456 Oak Ave", "city": "Lyon"},
            ],
        }

    def create_csv_file(self, content, filename="test.csv"):
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    def test_get_request_renders_form(self, mock_import, mock_messages):
        get_request = self.factory.get("/admin/services/service/import-services/")

        response = self.service_admin.import_services_view(get_request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Importer des Services d&#x27;un CSV")
        self.assertContains(response, "csv_file")
        self.assertContains(response, "wet_run")
        self.assertContains(response, "source_label")

        mock_messages.error.assert_not_called()
        mock_messages.success.assert_not_called()
        mock_messages.warning.assert_not_called()

    # Les tests de la validation du csv
    def test_post_without_file(self, mock_import, mock_messages):
        response = self.service_admin.import_services_view(self.post_request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            self.post_request, "Veuillez sélectionner un fichier CSV."
        )
        mock_import.assert_not_called()

    def test_post_with_non_csv_file(self, mock_import, mock_messages):
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": txt_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request, "Veuillez télécharger un fichier CSV valide."
        )
        mock_import.assert_not_called()

    def test_post_with_oversized_file(self, mock_import, mock_messages):
        large_content = "a" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.csv", large_content.encode("utf-8"), content_type="text/csv"
        )

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": large_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request, "Le fichier est trop volumineux (maximum 10MB)."
        )
        mock_import.assert_not_called()

    def test_post_with_invalid_encoding(self, mock_import, mock_messages):
        mock_import.side_effect = UnicodeDecodeError(
            "utf-8", b"invalid", 0, 1, "Invalid UTF-8 sequence"
        )

        invalid_file = SimpleUploadedFile(
            "invalid.csv",
            b"invalid",
            content_type="text/csv",
        )

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": invalid_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request,
            "Erreur d'encodage du fichier. Assurez-vous que le fichier est encodé en UTF-8.",
        )

    # Les tests de l'info de la source
    def test_source_info_with_simple_filename(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "simple.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": "Test Label"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2], {"value": "simple", "label": "Test Label"}
        )
        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 5 nouveaux services."
        )
        self.assertEqual(response.url, "..")

    def test_source_info_with_complex_filename(self, mock_import, mock_messages):
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "monthly.import.2024.01.csv")

        mock_import.return_value = self.mock_success_result

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": "Complex Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "monthly.import.2024.01", "label": "Complex Test"},
        )
        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 5 nouveaux services."
        )
        self.assertEqual(response.url, "..")

    def test_source_info_with_empty_label(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "test.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": ""},
        )
        request.user = self.user

        self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "test", "label": "Importé de l'admin"},
        )
        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 5 nouveaux services."
        )

    def test_source_info_with_whitespace_label(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "test.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": "   "},
        )
        request.user = self.user

        self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "test", "label": "Importé de l'admin"},
        )
        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 5 nouveaux services."
        )

    # Les Tests de Wet Run vs Dry Run
    def test_wet_run_success(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": "Wet Run Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_import.assert_called_once()
        call_args = mock_import.call_args
        self.assertEqual(call_args[0][1], self.user)
        self.assertTrue(call_args[1]["wet_run"])

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 5 nouveaux services."
        )

    def test_dry_run_success(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {
                "csv_file": csv_file,
                "wet_run": False,
                "source_label": "Dry Run Test",
            },
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_import.assert_called_once()
        call_args = mock_import.call_args
        self.assertFalse(call_args[1]["wet_run"])

        mock_messages.success.assert_called_once_with(
            request,
            "Votre import de test est fini. Vous auriez créé 5 nouveaux services.",
        )

    def test_wet_run_with_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on", "source_label": "Error Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.info.assert_called_once_with(
            request, "Import terminé avec 0 services créés."
        )
        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "Il faut résoudre les erreurs suivantes avant que vous puissiez faire l'import :<br/>"
                "• Ligne 2 : SIRET manquant.<br/>"
                "• Ligne 3 : Structure introuvable."
            ),
        )

    def test_dry_run_with_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "source_label": "Dry Run Error Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.success.assert_called_once_with(
            request,
            "Votre import de test est fini. Vous auriez créé 0 nouveaux services.",
        )
        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "Il faut résoudre les erreurs suivantes avant que vous puissiez faire l'import :<br/>"
                "• Ligne 2 : SIRET manquant.<br/>"
                "• Ligne 3 : Structure introuvable."
            ),
        )

    # Les tests pour les messages d'erreur d'avertissement
    def test_error_messages(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.info.assert_called_once_with(
            request, "Import terminé avec 0 services créés."
        )
        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "Il faut résoudre les erreurs suivantes avant que vous puissiez faire l'import :<br/>"
                "• Ligne 2 : SIRET manquant.<br/>"
                "• Ligne 3 : Structure introuvable."
            ),
        )

    def test_duplicate_services_warning(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": ["Service A", "Service B"],
            "geo_data_missing_lines": [],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 1 nouveaux services."
        )
        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "Certains services sont déjà présents dans la base de données :<br/>"
                "• Service A<br/>"
                "• Service B"
            ),
        )

    def test_geo_missing_warning(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [
                {"idx": 1, "address": "123 Main St", "city": "Paris"},
                {"idx": 3, "address": "456 Oak Ave", "city": "Lyon"},
            ],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 1 nouveaux services."
        )
        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "Certains services n'ont pas pu être géolocalisés :<br/>"
                "• Ligne 1 - 123 Main St<br/>"
                "• Ligne 3 - 456 Oak Ave"
            ),
        )

    def test_combined_warnings(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_warning_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 3 nouveaux services."
        )
        mock_messages.warning.assert_any_call(
            request,
            mark_safe(
                "Certains services sont déjà présents dans la base de données :<br/>"
                "• Service A<br/>"
                "• Service B"
            ),
        )
        mock_messages.warning.assert_any_call(
            request,
            mark_safe(
                "Certains services n'ont pas pu être géolocalisés :<br/>"
                "• Ligne 1 - 123 Main St<br/>"
                "• Ligne 3 - 456 Oak Ave"
            ),
        )

    # Tests de la gestion des exceptions
    def test_import_function_raises_exception(self, mock_import, mock_messages):
        mock_import.side_effect = Exception("Unexpected error")

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request, "Une erreur inattendue s'est produite : Unexpected error"
        )

    # Edge Cases
    def test_missing_result_keys(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1
        }  # Les autres clés sont manquantes

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 1 nouveaux services."
        )

    def test_geo_data_missing_address_key(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [{"idx": 1}],  # La clé 'address' est manquante
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "wet_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request, "Votre import a réussi. Vous avez créé 1 nouveaux services."
        )
        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "Certains services n'ont pas pu être géolocalisés :<br/>"
                "• Ligne 1 - Adresse inconnue"
            ),
        )
