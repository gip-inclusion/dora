from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework.test import APIClient

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import EPCI, City


class SearchEpcisAndCitiesViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.lyon = City.objects.create(
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
        cls.marseille = City.objects.create(
            code="13055",
            name="Marseille",
            department="13",
            epci="200054807",
            region="93",
            postal_codes=["13001"],
            population=870731,
            normalized_name="MARSEILLE",
            center=Point(5.3698, 43.2965, srid=WGS84),
        )

        cls.metropole_lyon = EPCI.objects.create(
            code="200046977",
            name="Métropole de Lyon",
            departments=["69"],
            regions=["84"],
            normalized_name="METROPOLE DE LYON",
        )
        cls.epci_multi = EPCI.objects.create(
            code="200070340",
            name="CC des Deux Rives",
            departments=["45", "89"],
            regions=["24", "27"],
            normalized_name="CC DES DEUX RIVES",
        )

    def test_matches_city_on_name(self):
        response = self.client.get("/admin-division-search-epcis-cities/?q=Lyon")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {"label": "Lyon", "value": ["69123"]},
            response.json()["cities"],
        )

    def test_matches_epci_on_name(self):
        response = self.client.get("/admin-division-search-epcis-cities/?q=Deux Rives")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {"label": "CC des Deux Rives", "value": ["45", "89"]},
            response.json()["epcis"],
        )

    def test_matches_epci_on_code(self):
        response = self.client.get("/admin-division-search-epcis-cities/?q=200070340")
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            {"label": "CC des Deux Rives", "value": ["45", "89"]},
            response.json()["epcis"],
        )

    def test_no_match(self):
        response = self.client.get("/admin-division-search-epcis-cities/?q=Zzzzzzzz")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"cities": [], "epcis": []})

    def test_q_is_required(self):
        response = self.client.get("/admin-division-search-epcis-cities/")
        self.assertEqual(response.status_code, 400)

    def test_caps_total_results(self):
        for i in range(8):
            City.objects.create(
                code=f"6900{i}",
                name=f"Lyonnet {i}",
                department="69",
                epci="",
                region="84",
                postal_codes=[],
                population=1000 - i,
                normalized_name=f"LYONNET {i}",
                center=Point(4.8, 45.7, srid=WGS84),
            )
            EPCI.objects.create(
                code=f"20000000{i}",
                name=f"CC Lyonnaise {i}",
                departments=["69"],
                regions=["84"],
                normalized_name=f"CC LYONNAISE {i}",
            )

        response = self.client.get("/admin-division-search-epcis-cities/?q=Lyon")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(len(data["cities"]) + len(data["epcis"]), 10)
