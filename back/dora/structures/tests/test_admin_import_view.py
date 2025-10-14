from unittest.mock import patch

from django.test import RequestFactory
from model_bakery import baker
from rest_framework.test import APITestCase

from config.admin import AdminSite
from dora.structures.admin import StructureAdmin
from dora.structures.models import Structure


class ImportStructuresViewTestCase(APITestCase):
    def setUp(self):
        self.user = baker.make("users.User", is_valid=True)

        self.admin_site = AdminSite()
        self.structure_admin = StructureAdmin(Structure, self.admin_site)

        self.factory = RequestFactory()

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

    @patch("dora.structures.admin.render")
    def test_get_request_without_job_id(self, mock_render):
        get_request = self.factory.get("/admin/structures/structure/import-structures/")

        self.structure_admin.import_structures_view(get_request)

        mock_render.assert_called_once()

        call_args = mock_render.call_args

        self.assertEqual(call_args[0][0], get_request)
        self.assertEqual(call_args[0][1], "admin/import_csv_form.html")
        self.assertEqual(call_args[0][2]["title"], "Module d'import de structures")
        self.assertFalse(hasattr(call_args[0][2], "job_id"))

    @patch("dora.structures.admin.render")
    def test_get_request_with_job_id(self, mock_render):
        get_request = self.factory.get(
            "/admin/structures/structure/import-structures/?job_id=12345"
        )

        self.structure_admin.import_structures_view(get_request)

        mock_render.assert_called_once()

        call_args = mock_render.call_args

        self.assertEqual(call_args[0][0], get_request)
        self.assertEqual(call_args[0][1], "admin/import_csv_form.html")
        self.assertEqual(call_args[0][2]["title"], "Module d'import de structures")
        self.assertEqual(call_args[0][2]["job_id"], "12345")

    @patch("dora.structures.admin.BaseImportAdminMixin.import_csv")
    def test_post_request_imports_csv(self, mock_import_csv):
        request = self.factory.post(
            "/admin/structures/service/import-services/",
        )
        request.user = self.user

        self.structure_admin.import_structures_view(request)

        mock_import_csv.assert_called_once()
        self.assertEqual(mock_import_csv.call_args[0][0], request)

    def test_successful_wet_run_with_no_errors(self):
        formatted_results = self.structure_admin.format_results(
            self.successful_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "success",
                    "message": "<b>Import terminé avec succès</b><br/>5 nouvelles structures ont été créées.<br/>"
                    "2 structures existantes ont été modifiées.<br/>"
                    "3 nouveaux services ont été crées en brouillon.<br/>",
                }
            ],
        )

    def test_successful_dry_run_with_no_errors(self):
        formatted_results = self.structure_admin.format_results(
            self.successful_result, is_wet_run=False
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "success",
                    "message": "<b>Import de test terminé avec succès</b><br/>",
                }
            ],
        )

    def test_import_with_errors_wet_run(self):
        formatted_results = self.structure_admin.format_results(
            self.error_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": "<b>Échec de l'import - Erreurs rencontrées</b><br/>"
                    "[2]: Nom requis, Email invalide<br/>"
                    "[5]: Structure déjà existante",
                }
            ],
        )

    def test_import_with_errors_dry_run(self):
        formatted_results = self.structure_admin.format_results(
            self.error_result, is_wet_run=False
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": "<b>Test terminé - Erreurs rencontrées</b><br/>"
                    "[2]: Nom requis, Email invalide<br/>"
                    "[5]: Structure déjà existante",
                }
            ],
        )
