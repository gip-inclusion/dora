import io
from unittest import mock

import pytest
import requests
from django.core.management import call_command
from django.test import SimpleTestCase, TestCase

from .api_client import DecoupageAdministratifAPIClient
from .importer import DecoupageAdministratifImporter, _parse_center
from .models import EPCI, City, Department, Region


@pytest.mark.no_django_db
class DecoupageAdministratifAPIClientTests(SimpleTestCase):
    def setUp(self):
        self.session = mock.Mock()
        self.response = mock.Mock()
        self.response.json.return_value = [{"code": "dummy"}]
        self.response.raise_for_status.return_value = None
        self.session.get.return_value = self.response
        self.client = DecoupageAdministratifAPIClient(
            base_url="https://example.com",
            timeout_seconds=5,
            session=self.session,
        )

    def test_fetch_communes_calls_expected_endpoint(self):
        data = self.client.fetch_communes()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/communes",
            params={
                "fields": "code,nom,codeDepartement,codeRegion,codesPostaux,codeEpci,population,centre",
                "format": "json",
            },
            timeout=5,
        )

    def test_fetch_departements_calls_expected_endpoint(self):
        data = self.client.fetch_departements()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/departements",
            params={"fields": "code,nom,codeRegion", "format": "json"},
            timeout=5,
        )

    def test_fetch_epci_calls_expected_endpoint(self):
        data = self.client.fetch_epci()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/epcis",
            params={
                "fields": "code,nom,codesDepartements,codesRegions",
                "format": "json",
            },
            timeout=5,
        )

    def test_fetch_regions_calls_expected_endpoint(self):
        data = self.client.fetch_regions()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/regions",
            params={"fields": "code,nom", "format": "json"},
            timeout=5,
        )

    def test_fetch_communes_propagates_http_errors(self):
        http_error = requests.HTTPError("boom")
        self.response.raise_for_status.side_effect = http_error

        with self.assertRaises(requests.HTTPError):
            self.client.fetch_communes()


class DecoupageAdministratifImporterTests(TestCase):
    def setUp(self):
        self.client = mock.Mock()
        self.importer = DecoupageAdministratifImporter(client=self.client)

    def test_import_regions_updates_names(self):
        Region.objects.create(code="44", name="Old Name")
        self.client.fetch_regions.return_value = [
            {"code": "44", "nom": "Grand Est"},
            {"code": "01", "nom": "Guadeloupe"},
        ]

        self.importer.import_regions()

        self.assertEqual(Region.objects.count(), 2)
        self.assertEqual(Region.objects.get(code="44").name, "Grand Est")
        self.assertEqual(Region.objects.get(code="01").name, "Guadeloupe")

    def test_import_departements_sets_region_codes(self):
        Region.objects.create(code="11", name="Île-de-France")
        self.client.fetch_departements.return_value = [
            {"code": "75", "nom": "Paris", "codeRegion": "11"},
        ]

        self.importer.import_departements()

        department = Department.objects.get(code="75")
        self.assertEqual(department.name, "Paris")
        self.assertEqual(department.region, "11")

    def test_import_epci_defaults_empty_lists(self):
        self.client.fetch_epci.return_value = [
            {
                "code": "200069193",
                "nom": "Métropole de Lyon",
                # intentionally missing optional fields
            }
        ]

        self.importer.import_epci()

        epci = EPCI.objects.get(code="200069193")
        self.assertEqual(epci.departments, [])
        self.assertEqual(epci.regions, [])

    def test_import_communes_handles_missing_values(self):
        self.client.fetch_communes.return_value = [
            {
                "code": "75056",
                "nom": "Paris",
                "codesPostaux": ["75001"],
            }
        ]

        self.importer.import_communes()

        city = City.objects.get(code="75056")
        self.assertEqual(city.department, "")
        self.assertEqual(city.epci, "")
        self.assertEqual(city.region, "")
        self.assertEqual(city.postal_codes, ["75001"])
        self.assertEqual(city.population, 0)
        self.assertIsNone(city.center)

    def test_import_communes_sets_population_and_center(self):
        self.client.fetch_communes.return_value = [
            {
                "code": "75056",
                "nom": "Paris",
                "codeDepartement": "75",
                "codeRegion": "11",
                "codeEpci": "200054781",
                "codesPostaux": ["75001"],
                "population": 2161000,
                "centre": {"type": "Point", "coordinates": [2.347, 48.8589]},
            }
        ]

        self.importer.import_communes()

        city = City.objects.get(code="75056")
        self.assertEqual(city.population, 2161000)
        self.assertIsNotNone(city.center)
        self.assertAlmostEqual(city.center.x, 2.347, places=3)
        self.assertAlmostEqual(city.center.y, 48.8589, places=3)

    def test_import_regions_sets_normalized_name(self):
        self.client.fetch_regions.return_value = [
            {"code": "44", "nom": "Grand Est"},
        ]

        self.importer.import_regions()

        region = Region.objects.get(code="44")
        self.assertEqual(region.normalized_name, "GRAND EST")

    def test_import_departements_sets_normalized_name(self):
        self.client.fetch_departements.return_value = [
            {"code": "75", "nom": "Paris", "codeRegion": "11"},
        ]

        self.importer.import_departements()

        department = Department.objects.get(code="75")
        self.assertEqual(department.normalized_name, "PARIS")

    def test_import_epci_sets_normalized_name(self):
        self.client.fetch_epci.return_value = [
            {
                "code": "200054781",
                "nom": "Métropole du Grand Paris",
                "codesDepartements": ["75"],
                "codesRegions": ["11"],
            }
        ]

        self.importer.import_epci()

        epci = EPCI.objects.get(code="200054781")
        self.assertEqual(epci.normalized_name, "METROPOLE DU GRAND PARIS")

    def test_import_communes_sets_normalized_name_with_department(self):
        self.client.fetch_communes.return_value = [
            {
                "code": "75056",
                "nom": "Paris",
                "codeDepartement": "75",
                "codeRegion": "11",
                "codesPostaux": ["75001"],
            }
        ]

        self.importer.import_communes()

        city = City.objects.get(code="75056")
        self.assertIn("PARIS", city.normalized_name)
        self.assertIn("75", city.normalized_name)

    def test_import_all_runs_every_step(self):
        with (
            mock.patch.object(self.importer, "import_regions") as import_regions,
            mock.patch.object(
                self.importer, "import_departements"
            ) as import_departements,
            mock.patch.object(self.importer, "import_epci") as import_epci,
            mock.patch.object(self.importer, "import_communes") as import_communes,
        ):
            self.importer.import_all()

        import_regions.assert_called_once_with()
        import_departements.assert_called_once_with()
        import_epci.assert_called_once_with()
        import_communes.assert_called_once_with()


@pytest.mark.no_django_db
class ParseCenterTests(SimpleTestCase):
    def test_parse_center_with_valid_point(self):
        center_data = {"type": "Point", "coordinates": [2.347, 48.8589]}

        result = _parse_center(center_data)

        self.assertIsNotNone(result)
        self.assertAlmostEqual(result.x, 2.347, places=3)
        self.assertAlmostEqual(result.y, 48.8589, places=3)

    def test_parse_center_with_none(self):
        self.assertIsNone(_parse_center(None))

    def test_parse_center_with_empty_dict(self):
        self.assertIsNone(_parse_center({}))

    def test_parse_center_with_wrong_type(self):
        center_data = {"type": "Polygon", "coordinates": [[0, 0], [1, 1]]}
        self.assertIsNone(_parse_center(center_data))

    def test_parse_center_with_missing_coordinates(self):
        center_data = {"type": "Point"}
        self.assertIsNone(_parse_center(center_data))

    def test_parse_center_with_invalid_coordinates(self):
        center_data = {"type": "Point", "coordinates": [2.347]}
        self.assertIsNone(_parse_center(center_data))


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
