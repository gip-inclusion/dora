from unittest.mock import patch

from django.contrib.admin.sites import AdminSite
from django.test import RequestFactory
from django.utils.html import format_html
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.services.admin import ServiceAdmin
from dora.services.models import Service


class ImportServicesViewTestCase(APITestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = baker.make("users.User", is_valid=True)

        self.admin_site = AdminSite()
        self.service_admin = ServiceAdmin(Service, self.admin_site)

        self.post_request = self.factory.post(
            "/admin/services/service/import-services/"
        )
        self.post_request.user = self.user

        self.service_admin = ServiceAdmin(Service, AdminSite())
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

    @patch("dora.services.admin.render")
    def test_get_request_without_job_id(self, mock_render):
        get_request = self.factory.get("/admin/services/service/import-services/")

        self.service_admin.import_services_view(get_request)

        mock_render.assert_called_once()

        call_args = mock_render.call_args

        self.assertEqual(call_args[0][0], get_request)
        self.assertEqual(call_args[0][1], "admin/import_csv_form.html")
        self.assertEqual(call_args[0][2]["title"], "Module d'import de services")
        self.assertFalse(hasattr(call_args[0][2], "job_id"))

    @patch("dora.services.admin.render")
    def test_get_request_with_job_id(self, mock_render):
        get_request = self.factory.get(
            "/admin/services/service/import-services/?job_id=12345"
        )

        self.service_admin.import_services_view(get_request)

        mock_render.assert_called_once()

        call_args = mock_render.call_args

        self.assertEqual(call_args[0][0], get_request)
        self.assertEqual(call_args[0][1], "admin/import_csv_form.html")
        self.assertEqual(call_args[0][2]["title"], "Module d'import de services")
        self.assertEqual(call_args[0][2]["job_id"], "12345")

    @patch("dora.services.admin.BaseImportAdminMixin.import_csv")
    def test_post_request_imports_csv(self, mock_import_csv):
        request = self.factory.post(
            "/admin/services/service/import-services/",
        )
        request.user = self.user

        self.service_admin.import_services_view(request)

        mock_import_csv.assert_called_once()
        self.assertEqual(mock_import_csv.call_args[0][0], request)

    # Les tests pour les messages de succès/erreur/avertissement
    def test_wet_run_success(self):
        formatted_results = self.service_admin.format_results(
            self.mock_success_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "success",
                    "message": "<b>Import terminé avec succès</b><br/>5 nouveaux services ont été créés et publiés",
                }
            ],
        )

    def test_dry_run_success(self):
        formatted_results = self.service_admin.format_results(
            self.mock_success_result, is_wet_run=False
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "success",
                    "message": "<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! 5 sont prêts à être importés et publiés.",
                }
            ],
        )

    def test_wet_run_with_errors(self):
        formatted_results = self.service_admin.format_results(
            self.mock_error_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": format_html(
                        "<b>Échec de l'import</b><br/>Aucun service n’a été importé, car le fichier comporte des erreurs. Veuillez corriger les éléments suivants :<br/>"
                        "• [2] SIRET manquant.<br/>"
                        "• [3] Structure introuvable."
                    ),
                }
            ],
        )

    def test_dry_run_with_errors(self):
        formatted_results = self.service_admin.format_results(
            self.mock_error_result, is_wet_run=False
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": format_html(
                        "<b>Test terminé - Erreurs à corriger</b><br/>Le fichier contient des erreurs qui empêcheront l'import. Veuillez corriger les éléments suivants :<br/>"
                        "• [2] SIRET manquant.<br/>"
                        "• [3] Structure introuvable."
                    ),
                }
            ],
        )

    # Les tests pour les messages d'erreur d'avertissement
    def test_error_messages(self):
        formatted_results = self.service_admin.format_results(
            self.mock_error_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": format_html(
                        "<b>Échec de l'import</b><br/>Aucun service n’a été importé, car le fichier comporte des erreurs. Veuillez corriger les éléments suivants :<br/>"
                        "• [2] SIRET manquant.<br/>"
                        "• [3] Structure introuvable."
                    ),
                }
            ],
        )

    def test_missing_header_messages(self):
        mock_result = {
            "missing_headers": ["header1", "header2"],
        }

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "error",
                    "message": "<b>Échec de l'import - Colonnes manquantes</b><br/>Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>"
                    "• header1<br/>"
                    "• header2",
                }
            ],
        )

    def test_duplicate_services_warning(self):
        mock_result = {
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

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 2)
        self.assertEqual(formatted_results[0]["level"], "success")
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Import réalisé - Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                    '• [2] SIRET 1234 - il existe déjà un service avec le modèle slug_1 et le courriel "a@a.com"<br/>'
                    '• [3] SIRET 3456 - il existe déjà un service avec le modèle slug_2 et le courriel "b@b.com"'
                ),
            },
        )

    def test_geo_missing_warning(self):
        mock_result = {
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

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 2)
        self.assertEqual(
            formatted_results[0],
            {
                "level": "success",
                "message": "<b>Import terminé avec succès</b><br/>1 nouveaux services ont été créés et publiés",
            },
        )
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                    "• [2] 123 Main St 75001 Paris<br/>"
                    "• [3] 456 Oak Ave 69001 Lyon"
                ),
            },
        )

    def test_combined_warnings_when_wet_run_with_errors(self):
        mock_result = {
            "created_count": 3,
            "errors": ["[2] Siret manquant"],
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
            "draft_services_created": [
                {
                    "idx": 1,
                    "name": "Service Test",
                    "missing_fields": ["contact email", "lieu de déroulement"],
                }
            ],
        }

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 5)
        self.assertEqual(formatted_results[0]["level"], "error")
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": "<b>D'autres irrégularités non bloquantes ont été détectées :</b>",
            },
        )
        self.assertEqual(
            formatted_results[2],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                    '• [2] SIRET 1234 - il existe déjà un service avec le modèle slug_1 et le courriel "a@a.com"<br/>'
                    '• [3] SIRET 3456 - il existe déjà un service avec le modèle slug_2 et le courriel "b@b.com"'
                ),
            },
        )
        self.assertEqual(
            formatted_results[3],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                    "• [1] 123 Main St  Paris<br/>"
                    "• [3] 456 Oak Ave  Lyon"
                ),
            },
        )
        self.assertEqual(
            formatted_results[4],
            {
                "level": "warning",
                "message": format_html(
                    '<b>Informations manquantes</b><br/> Contactez les structures pour compléter ces éléments avant importation :<br/>• [1] Service "Service Test" - Manque : contact email, lieu de déroulement'
                ),
            },
        )

    def test_combined_warnings_when_wet_run_no_errors(self):
        mock_result = {
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
            "draft_services_created": [
                {
                    "idx": 1,
                    "name": "Service Test",
                    "missing_fields": ["contact email", "lieu de déroulement"],
                }
            ],
        }

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 4)
        self.assertEqual(formatted_results[0]["level"], "success")
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Import réalisé - Doublons potentiels détectés</b><br/>Nous avons détecté des similitudes avec des services existants. Nous vous recommandons de vérifier :<br/>"
                    '• [2] SIRET 1234 - il existe déjà un service avec le modèle slug_1 et le courriel "a@a.com"<br/>'
                    '• [3] SIRET 3456 - il existe déjà un service avec le modèle slug_2 et le courriel "b@b.com"'
                ),
            },
        )
        self.assertEqual(
            formatted_results[2],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                    "• [1] 123 Main St  Paris<br/>"
                    "• [3] 456 Oak Ave  Lyon"
                ),
            },
        )
        self.assertEqual(
            formatted_results[3],
            {
                "level": "warning",
                "message": format_html(
                    '<b>Import réalisé - Services importés en brouillon</b><br/>1 services ont été importés en brouillon. Contactez les structures pour compléter ces éléments avant publication :<br/>• [1] Service "Service Test" - Manque : contact email, lieu de déroulement'
                ),
            },
        )

    def test_missing_fields_for_publishing_wet_run(self):
        mock_result = {
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

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 2)
        self.assertEqual(
            formatted_results[0],
            {
                "level": "success",
                "message": "<b>Import terminé avec succès</b><br/>4 nouveaux services ont été créés et publiés",
            },
        )
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": "<b>Import réalisé - Services importés en brouillon</b><br/>1 services ont été importés en brouillon. Contactez les structures pour compléter ces éléments avant publication :<br/>"
                '• [1] Service "Service Test" - Manque : contact email, lieu de déroulement',
            },
        )

    def test_missing_fields_for_publishing_dry_run(self):
        mock_result = {
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

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=False
        )

        self.assertEqual(len(formatted_results), 2)
        self.assertEqual(
            formatted_results[0],
            {
                "level": "success",
                "message": "<b>Test réalisé avec succès - aucune erreur détectée</b><br/>C'est tout bon ! 4 sont prêts à être importés et publiés.",
            },
        )
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": "<b>Test terminé - Services incomplets</b><br/>1 services seront passés en brouillon en cas d'import. Contactez les structures pour compléter ces éléments avant importation :<br/>"
                '• [1] Service "Service Test" - Manque : contact email, lieu de déroulement',
            },
        )

    # Edge Cases
    def test_missing_result_keys(self):
        mock_result = {"created_count": 1}  # Les autres clés sont manquantes

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(
            formatted_results,
            [
                {
                    "level": "success",
                    "message": "<b>Import terminé avec succès</b><br/>1 nouveaux services ont été créés et publiés",
                }
            ],
        )

    def test_geo_data_missing_address_key(self):
        mock_result = {
            "created_count": 1,
            "errors": [],
            "duplicated_services": [],
            "geo_data_missing_lines": [
                {"idx": 1, "address": "1 rue de test"}
            ],  # Les clés 'city' et 'code_postal sont manquantes
        }

        formatted_results = self.service_admin.format_results(
            mock_result, is_wet_run=True
        )

        self.assertEqual(len(formatted_results), 2)
        self.assertEqual(formatted_results[0]["level"], "success")
        self.assertEqual(
            formatted_results[1],
            {
                "level": "warning",
                "message": format_html(
                    "<b>Import réalisé - Géolocalisation incomplète</b><br/>Certaines adresses n'ont pas pu être géolocalisées correctement et risquent de ne pas apparaître dans les résultats de recherche :<br/>"
                    "• [1] 1 rue de test  "
                ),
            },
        )
