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
@patch("dora.services.admin.ImportServicesHelper.import_services")
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
            "draft_services_created": [],
        }
        self.mock_error_result = {
            "created_count": 0,
            "errors": [
                "[2] SIRET manquant.",
                "[3] Structure introuvable.",
            ],
            "duplicated_services": [],
            "geo_data_missing_lines": [],
            "draft_services_created": [],
        }
        self.mock_warning_result = {
            "created_count": 3,
            "errors": [],
            "duplicated_services": [
                {
                    "idx": 2,
                    "siret": "1234",
                    "name": "Service A",
                    "model_slug": "slug_1",
                    "contact_email": "a@a.com",
                },
                {
                    "idx": 3,
                    "siret": "3456",
                    "name": "Service B",
                    "model_slug": "slug_2",
                    "contact_email": "b@b.com",
                },
            ],
            "geo_data_missing_lines": [
                {"idx": 1, "address": "123 Main St", "city": "Paris"},
                {"idx": 3, "address": "456 Oak Ave", "city": "Lyon"},
            ],
            "draft_services_created": [],
        }

    def create_csv_file(self, content, filename="test.csv"):
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    @patch("dora.core.mixins.messages")
    def test_get_request_renders_form(self, mock_messages, mock_import, _):
        get_request = self.factory.get("/admin/services/service/import-services/")

        response = self.service_admin.import_services_view(get_request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Module d&#x27;import de services")
        self.assertContains(response, "csv_file")
        self.assertContains(response, "test_run")
        self.assertContains(response, "source_label")

        mock_messages.error.assert_not_called()
        mock_messages.success.assert_not_called()
        mock_messages.warning.assert_not_called()

    # Les tests de la validation du csv
    @patch("dora.core.mixins.messages")
    def test_post_without_file(self, mock_messages, mock_import, _):
        response = self.service_admin.import_services_view(self.post_request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            self.post_request, "Veuillez sélectionner un fichier CSV."
        )
        mock_import.assert_not_called()

    @patch("dora.core.mixins.messages")
    def test_post_with_non_csv_file(self, mock_messages, mock_import, _):
        txt_file = SimpleUploadedFile(
            "test.txt", b"not a csv file", content_type="text/plain"
        )

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": txt_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Format de fichier non valide</b><br/>Le fichier n'est pas au format CSV attendu. Assurez-vous d'utiliser un fichier .csv avec des colonnes séparées par des virgules.",
        )
        mock_import.assert_not_called()

    @patch("dora.core.mixins.messages")
    def test_post_with_oversized_file(self, mock_messages, mock_import, _):
        large_content = "a" * (11 * 1024 * 1024)  # 11MB
        large_file = SimpleUploadedFile(
            "large.csv", large_content.encode("utf-8"), content_type="text/csv"
        )

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": large_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Fichier trop volumineux</b><br/>Le fichier doit être moins de 10MB.",
        )
        mock_import.assert_not_called()

    @patch("dora.core.mixins.messages")
    def test_post_with_invalid_encoding(self, mock_messages, mock_import, _):
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
            {"csv_file": invalid_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")
        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Erreur d'encodage du fichier</b><br/>Le fichier contient des caractères spéciaux illisibles. Sauvegardez votre fichier en UTF-8 et relancez l'import.",
        )

    # Les tests de l'info de la source
    def test_source_info_with_simple_filename(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "simple.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": "Test Label"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2], {"value": "simple", "label": "Test Label"}
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
        )
        self.assertEqual(response.url, "..")

    def test_source_info_with_complex_filename(self, mock_import, mock_messages):
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "monthly.import.2024.01.csv")

        mock_import.return_value = self.mock_success_result

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": "Complex Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "monthly.import.2024.01", "label": "Complex Test"},
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
        )
        self.assertEqual(response.url, "..")

    def test_source_info_with_empty_label(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "test.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": ""},
        )
        request.user = self.user

        self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "test", "label": "DORA"},
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
        )

    def test_source_info_with_whitespace_label(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result
        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content, "test.csv")

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": "   "},
        )
        request.user = self.user

        self.service_admin.import_services_view(request)

        self.assertEqual(
            mock_import.call_args[0][2],
            {"value": "test", "label": "DORA"},
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
        )

    # Les Tests de Configuration (Wet Run / Dry Run; Supprimer les 2 premières lignes)
    def test_wet_run_success(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": "Wet Run Test"},
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
            request,
            "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
        )

    def test_dry_run_success(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {
                "csv_file": csv_file,
                "test_run": "on",
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
            "<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! 5 sont prêts à être importés et publiés.",
        )

    def test_wet_run_with_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off", "source_label": "Error Test"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "<b>Échec de l'import - Erreurs à corriger</b><br/>Le fichier contient des erreurs qui empêchent l'import. Veuillez corriger les éléments suivants :<br/>"
                "• [2] SIRET manquant.<br/>"
                "• [3] Structure introuvable."
            ),
        )

    def test_dry_run_with_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {
                "csv_file": csv_file,
                "test_run": "on",
                "source_label": "Dry Run Error Test",
            },
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "<b>Test terminé - Erreurs à corriger</b><br/>Le fichier contient des erreurs qui empêchent l'import. Veuillez corriger les éléments suivants :<br/>"
                "• [2] SIRET manquant.<br/>"
                "• [3] Structure introuvable."
            ),
        )

    def test_remove_instructions_lines(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_success_result

        csv_content = (
            "# This is a comment line\n"
            "# Another comment line\n"
            "header1,header2\n"
            "value1,value2"
        )
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {
                "csv_file": csv_file,
                "test_run": "off",
                "should_remove_instructions": "on",
            },
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_import.assert_called_once()
        self.assertTrue(mock_import.call_args.kwargs["should_remove_first_two_lines"])

    # Les tests pour les messages d'erreur d'avertissement
    def test_error_messages(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_error_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            mark_safe(
                "<b>Échec de l'import - Erreurs à corriger</b><br/>Le fichier contient des erreurs qui empêchent l'import. Veuillez corriger les éléments suivants :<br/>"
                "• [2] SIRET manquant.<br/>"
                "• [3] Structure introuvable."
            ),
        )
        mock_messages.success.assert_not_called()

    def test_missing_header_messages(self, mock_import, mock_messages):
        mock_import.return_value = {
            "missing_headers": ["header1", "header2"],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Colonnes manquantes</b><br/>Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>"
            "• header1<br/>"
            "• header2",
        )
        mock_messages.success.assert_not_called()

    def test_duplicate_services_warning(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [
                {
                    "idx": 2,
                    "siret": "1234",
                    "name": "Service A",
                    "model_slug": "slug_1",
                    "contact_email": "a@a.com",
                },
                {
                    "idx": 3,
                    "siret": "3456",
                    "model_slug": "slug_2",
                    "name": "Service B",
                    "contact_email": "b@b.com",
                },
            ],
            "geo_data_missing_lines": [],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "<b>Import réalisé - Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                '• [2] SIRET 1234 - il existe déjà un service avec le modèle slug_1 et le courriel "a@a.com"<br/>'
                '• [3] SIRET 3456 - il existe déjà un service avec le modèle slug_2 et le courriel "b@b.com"'
            ),
        )

    def test_geo_missing_warning(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [
                {
                    "idx": 2,
                    "address": "123 Main St",
                    "city": "Paris",
                    "postal_code": "75001",
                },
                {
                    "idx": 3,
                    "address": "456 Oak Ave",
                    "city": "Lyon",
                    "postal_code": "69001",
                },
            ],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>1 nouveaux services ont été créés et publiés",
        )
        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                "• [2] 123 Main St 75001 Paris<br/>"
                "• [3] 456 Oak Ave 69001 Lyon"
            ),
        )

    def test_combined_warnings(self, mock_import, mock_messages):
        mock_import.return_value = self.mock_warning_result

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.warning.assert_any_call(
            request,
            mark_safe(
                "<b>Import réalisé - Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                '• [2] SIRET 1234 - il existe déjà un service avec le modèle slug_1 et le courriel "a@a.com"<br/>'
                '• [3] SIRET 3456 - il existe déjà un service avec le modèle slug_2 et le courriel "b@b.com"'
            ),
        )
        mock_messages.warning.assert_any_call(
            request,
            mark_safe(
                "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                "• [1] 123 Main St  Paris<br/>"
                "• [3] 456 Oak Ave  Lyon"
            ),
        )

    def test_missing_fields_for_publishing_wet_run(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 5,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [],
            "draft_services_created": [
                {
                    "idx": 1,
                    "name": "Service Test",
                    "missing_fields": ["contact email", "lieu de déroulement"],
                }
            ],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.warning.assert_called_once_with(
            request,
            "<b>Import réalisé - Services importés en brouillon</b><br/>1 services ont été importés en brouillon. Contactez les structures pour compléter ces éléments avant publication :<br/>"
            '• [1] Service "Service Test" - Manque : contact email, lieu de déroulement',
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>4 nouveaux services ont été créés et publiés",
        )

    def test_missing_fields_for_publishing_dry_run(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 5,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [],
            "draft_services_created": [
                {
                    "idx": 1,
                    "name": "Service Test",
                    "missing_fields": ["contact email", "lieu de déroulement"],
                }
            ],
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "on"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.warning.assert_called_once_with(
            request,
            "<b>Test terminé - Services incomplets</b><br/>1 services seront passés en brouillon en cas d'import. Contactez les structures pour compléter ces éléments avant importation :<br/>"
            '• [1] Service "Service Test" - Manque : contact email, lieu de déroulement',
        )
        mock_messages.success.assert_called_once_with(
            request,
            "<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! 4 sont prêts à être importés et publiés.",
        )

    # Tests de la gestion des exceptions
    @patch("dora.core.mixins.messages")
    def test_import_function_raises_exception(self, mock_messages, mock_import, _):
        mock_import.side_effect = Exception("Unexpected error")

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            "<b>Échec de l'import - Erreur inattendue</b><br/>L'erreur suivante s'est produite :<br/>Unexpected error<br/>Si le problème persiste, contactez les développeurs.",
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
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request,
            "<b>Import terminé avec succès</b><br/>1 nouveaux services ont été créés et publiés",
        )

    def test_geo_data_missing_address_key(self, mock_import, mock_messages):
        mock_import.return_value = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [
                {"idx": 1, "address": "1 rue de test"}
            ],  # Les clés 'city' et 'code_postal sont manquantes
        }

        csv_content = "header1,header2\nvalue1,value2"
        csv_file = self.create_csv_file(csv_content)

        request = self.factory.post(
            "/admin/services/service/import-services/",
            {"csv_file": csv_file, "test_run": "off"},
        )
        request.user = self.user

        response = self.service_admin.import_services_view(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.warning.assert_called_once_with(
            request,
            mark_safe(
                "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                "• [1] 1 rue de test  "
            ),
        )
