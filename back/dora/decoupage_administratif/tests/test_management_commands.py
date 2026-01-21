import io
from unittest import mock

import pytest
from django.core.management import call_command
from django.test import SimpleTestCase


@pytest.mark.no_django_db
class ImportDecoupageAdministratifCommandTests(SimpleTestCase):
    @mock.patch(
        "dora.decoupage_administratif.management.commands.import_decoupage_administratif.DecoupageAdministratifImporter"
    )
    def test_command_runs_full_import_by_default(self, importer_cls):
        importer_instance = importer_cls.return_value

        call_command("import_decoupage_administratif")

        importer_instance.import_all.assert_called_once_with()

    @mock.patch(
        "dora.decoupage_administratif.management.commands.import_decoupage_administratif.DecoupageAdministratifImporter"
    )
    def test_command_supports_scope_argument(self, importer_cls):
        scopes_methods = {
            "regions": "import_regions",
            "departements": "import_departements",
            "epci": "import_epci",
            "communes": "import_communes",
            "all": "import_all",
        }

        for scope, method_name in scopes_methods.items():
            importer_instance = mock.Mock()
            importer_cls.return_value = importer_instance

            call_command("import_decoupage_administratif", scope=scope)

            getattr(importer_instance, method_name).assert_called_once_with()
            for other_method_name in scopes_methods.values():
                if other_method_name != method_name:
                    getattr(importer_instance, other_method_name).assert_not_called()

    @mock.patch(
        "dora.decoupage_administratif.management.commands.import_decoupage_administratif.DecoupageAdministratifImporter"
    )
    def test_command_calls_requested_scope_for_each_entity(self, importer_cls):
        importer_instance = importer_cls.return_value
        scopes_methods = {
            "communes": importer_instance.import_communes,
            "departements": importer_instance.import_departements,
            "epci": importer_instance.import_epci,
            "regions": importer_instance.import_regions,
            "all": importer_instance.import_all,
        }

        for scope, method in scopes_methods.items():
            importer_instance.reset_mock()
            call_command("import_decoupage_administratif", scope=scope)
            method.assert_called_once_with()

    @mock.patch(
        "dora.decoupage_administratif.management.commands.import_decoupage_administratif.DecoupageAdministratifImporter"
    )
    def test_command_prints_progress_messages(self, importer_cls):
        out = io.StringIO()
        call_command("import_decoupage_administratif", stdout=out)

        output = out.getvalue()
        self.assertIn("Démarrage de l'import 'all'...", output)
        self.assertIn("Import terminé.", output)
