from unittest.mock import patch

from django.core.files.uploadedfile import SimpleUploadedFile
from django.http import HttpResponseRedirect
from django.test import RequestFactory
from django.utils.html import format_html
from model_bakery import baker
from rest_framework.test import APITestCase

from config.admin import AdminSite
from dora.structures.admin import StructureAdmin
from dora.structures.models import Structure


@patch("dora.structures.admin.messages")
@patch("dora.structures.admin.ImportStructuresHelper.import_structures")
class ImportStructuresViewTestCase(APITestCase):
    def setUp(self):
        self.user = baker.make("users.User", is_valid=True)

        self.admin_site = AdminSite()
        self.structure_admin = StructureAdmin(Structure, self.admin_site)

        self.factory = RequestFactory()

        self.csv_headers = "nom,siret,siret_parent,courriels_administrateurs,labels,modeles,telephone,courriel_structure"
        self.csv_content = "header1,header2\nvalue1,value2"
        self.csv_file = self.create_csv_file(self.csv_content)
        self.successful_result = {
            "errors_map": {},
            "created_structures_count": 5,
            "created_services_count": 3,
            "edited_structures_count": 2,
        }
        self.error_result = {
            "errors_map": {
                2: ["Nom requis", "Email invalide"],
                5: ["Structure déjà existante"],
            },
            "created_structures_count": 0,
            "created_services_count": 0,
            "edited_structures_count": 0,
        }

    def create_csv_file(self, content, filename="test.csv"):
        return SimpleUploadedFile(
            filename, content.encode("utf-8"), content_type="text/csv"
        )

    @patch("dora.core.mixins.messages")
    def test_get_request_renders_form(self, mock_messages, mock_import, _):
        get_request = self.factory.get("/admin/structures/structure/import-structures/")

        response = self.structure_admin.import_structures_view(get_request)

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Module d&#x27;import de structures")
        self.assertContains(response, "csv_file")
        self.assertContains(response, "test_run")
        self.assertContains(response, "source_label")

        mock_messages.error.assert_not_called()
        mock_messages.success.assert_not_called()
        mock_messages.warning.assert_not_called()

    def test_successful_wet_run_with_no_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.successful_result

        request = self.factory.post(
            "/admin/structures/structure/import-structures/",
            {
                "csv_file": self.csv_file,
                "test_run": "off",
                "source_label": "Test Import",
            },
        )
        request.user = self.user

        response = self.structure_admin.import_structures_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, "..")

        mock_messages.success.assert_called_once_with(
            request,
            format_html(
                "<b>Import terminé avec succès</b><br/>5 nouvelles structures ont été créées.<br/>"
                "2 structures existantes ont été modifiées.<br/>"
                "3 nouveaux services ont été crées en brouillon.<br/>"
            ),
        )
        mock_messages.error.assert_not_called()

    def test_successful_dry_run_with_no_errors(self, mock_import, mock_messages):
        mock_import.return_value = self.successful_result

        request = self.factory.post(
            "/admin/structures/structure/import-structures/",
            {
                "csv_file": self.csv_file,
                "test_run": "on",
                "source_label": "Test Import",
            },
        )
        request.user = self.user

        response = self.structure_admin.import_structures_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.success.assert_called_once_with(
            request,
            format_html("<b>Import de test terminé avec succès</b><br/>"),
        )

        mock_messages.error.assert_not_called()

    def test_import_with_errors_wet_run(self, mock_import, mock_messages):
        mock_import.return_value = self.error_result

        request = self.factory.post(
            "/admin/structures/structure/import-structures/",
            {
                "csv_file": self.csv_file,
                "test_run": "off",
                "source_label": "Test Import",
            },
        )
        request.user = self.user

        response = self.structure_admin.import_structures_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            format_html(
                "<b>Échec de l'import - Erreurs rencontrées</b><br/>"
                "[2]: Nom requis, Email invalide<br/>"
                "[5]: Structure déjà existante"
            ),
        )

        mock_messages.success.assert_not_called()

    def test_import_with_errors_dry_run(self, mock_import, mock_messages):
        mock_import.return_value = self.error_result

        request = self.factory.post(
            "/admin/structures/structure/import-structures/",
            {
                "csv_file": self.csv_file,
                "test_run": "on",
                "source_label": "Test Import",
            },
        )
        request.user = self.user

        response = self.structure_admin.import_structures_view(request)
        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.url, ".")

        mock_messages.error.assert_called_once_with(
            request,
            format_html(
                "<b>Test terminé - Erreurs rencontrées</b><br/>"
                "[2]: Nom requis, Email invalide<br/>"
                "[5]: Structure déjà existante"
            ),
        )

        mock_messages.success.assert_not_called()
