from django.contrib.gis.geos import Point
from django.test import TestCase

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import EPCI, City, Department, Region
from dora.decoupage_administratif.utils import get_zone_eligibilite_choices


class ZoneEligibiliteChoicesTests(TestCase):
    """La zone d'éligibilité ne stocke que des codes : on doit pouvoir en
    redéduire les territoires que l'utilisateur avait sélectionnés."""

    @classmethod
    def setUpTestData(cls):
        Region.objects.create(code="84", name="Auvergne-Rhône-Alpes")
        Region.objects.create(code="11", name="Île-de-France")

        # une région à deux départements, pour pouvoir la reconstituer
        Department.objects.create(code="69", name="Rhône", region="84")
        Department.objects.create(code="01", name="Ain", region="84")
        # une région à un seul département
        Department.objects.create(code="75", name="Paris", region="11")

        City.objects.create(
            code="69123",
            name="Lyon",
            department="69",
            epci="200046977",
            region="84",
            postal_codes=["69001"],
            population=522969,
            normalized_name="LYON",
            center=Point(4.8357, 45.7640, srid=WGS84),
        )

    def test_returns_nothing_without_codes(self):
        self.assertEqual(get_zone_eligibilite_choices([]), [])
        self.assertEqual(get_zone_eligibilite_choices(None), [])

    def test_recognizes_a_department(self):
        self.assertEqual(
            get_zone_eligibilite_choices(["69"]),
            [{"label": "Rhône (69)", "type": "department", "codes": ["69"]}],
        )

    def test_recognizes_a_city(self):
        self.assertEqual(
            get_zone_eligibilite_choices(["69123"]),
            [{"label": "Lyon (69123)", "type": "city", "codes": ["69123"]}],
        )

    def test_recognizes_a_region_from_all_its_departments(self):
        self.assertEqual(
            get_zone_eligibilite_choices(["69", "01"]),
            [
                {
                    "label": "Auvergne-Rhône-Alpes",
                    "type": "region",
                    "codes": ["01", "69"],
                }
            ],
        )

    def test_keeps_departments_when_the_region_is_incomplete(self):
        # il manque l'Ain : ce n'est pas la région qui avait été sélectionnée
        self.assertEqual(
            get_zone_eligibilite_choices(["69"]),
            [{"label": "Rhône (69)", "type": "department", "codes": ["69"]}],
        )

    def test_mixes_region_departments_and_cities(self):
        self.assertEqual(
            get_zone_eligibilite_choices(["69", "01", "75", "69123"]),
            [
                {
                    "label": "Auvergne-Rhône-Alpes",
                    "type": "region",
                    "codes": ["01", "69"],
                },
                {"label": "Paris (75)", "type": "department", "codes": ["75"]},
                {"label": "Lyon (69123)", "type": "city", "codes": ["69123"]},
            ],
        )

    def test_ignores_unknown_codes(self):
        self.assertEqual(get_zone_eligibilite_choices(["99999", "ZZ"]), [])

    def test_keeps_the_department_of_a_single_department_region(self):
        # cas des DOM : la région et le département couvrent le même territoire
        # et sont enregistrés sous le même code, on ne peut pas les distinguer
        self.assertEqual(
            get_zone_eligibilite_choices(["75"]),
            [{"label": "Paris (75)", "type": "department", "codes": ["75"]}],
        )

    def test_recognizes_an_epci(self):
        EPCI.objects.create(
            code="200046977",
            name="Métropole de Lyon",
            departments=["69"],
            regions=["84"],
            normalized_name="METROPOLE DE LYON",
        )

        self.assertEqual(
            get_zone_eligibilite_choices(["200046977"]),
            [
                {
                    "label": "Métropole de Lyon",
                    "type": "epci",
                    "codes": ["200046977"],
                }
            ],
        )

    def test_mixes_every_division_type(self):
        EPCI.objects.create(
            code="200046977",
            name="Métropole de Lyon",
            departments=["69"],
            regions=["84"],
            normalized_name="METROPOLE DE LYON",
        )

        self.assertEqual(
            get_zone_eligibilite_choices(["69", "01", "75", "69123", "200046977"]),
            [
                {
                    "label": "Auvergne-Rhône-Alpes",
                    "type": "region",
                    "codes": ["01", "69"],
                },
                {"label": "Paris (75)", "type": "department", "codes": ["75"]},
                {
                    "label": "Métropole de Lyon",
                    "type": "epci",
                    "codes": ["200046977"],
                },
                {"label": "Lyon (69123)", "type": "city", "codes": ["69123"]},
            ],
        )

    def test_ignores_codes_of_an_unknown_format(self):
        # ni 2-3 caractères, ni 5, ni 9 chiffres
        self.assertEqual(
            get_zone_eligibilite_choices(["1", "123456", "abcdefghij"]), []
        )
