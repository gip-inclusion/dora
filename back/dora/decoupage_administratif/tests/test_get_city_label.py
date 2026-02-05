from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework.test import APIClient

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import City


class GetCityLabelViewTests(TestCase):
    """Tests pour l'endpoint /city-label/<insee_code>/ (vue get_city_label)."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.city_paris = City.objects.create(
            code="75056",
            name="Paris",
            department="75",
            region="11",
            epci="200055781",
            normalized_name="PARIS",
            center=Point(2.3522, 48.8566, srid=WGS84),
        )
        cls.city_lyon = City.objects.create(
            code="69123",
            name="Lyon",
            department="69",
            region="84",
            epci="200046977",
            normalized_name="LYON",
            center=Point(4.8357, 45.7640, srid=WGS84),
        )
        cls.city_ajaccio = City.objects.create(
            code="2A004",
            name="Ajaccio",
            department="2A",
            region="94",
            epci="200040947",
            normalized_name="AJACCIO",
            center=Point(8.7386, 41.9258, srid=WGS84),
        )

    def test_get_city_label_returns_city_name(self):
        """Le code 75056 retourne Paris."""
        response = self.client.get("/city-label/75056/")
        assert response.status_code == 200
        assert response.json() == "Paris"

    def test_get_city_label_lyon(self):
        """ "Le code 69123 retourne Lyon."""
        response = self.client.get("/city-label/69123/")
        assert response.status_code == 200
        assert response.json() == "Lyon"

    def test_get_city_label_corse_2a_uppercase(self):
        """Un code INSEE Corse en majuscules (2A) est correctement reconnu."""
        response = self.client.get("/city-label/2A004/")
        assert response.status_code == 200
        assert response.json() == "Ajaccio"

    def test_get_city_label_corse_2a_lowercase(self):
        """Un code INSEE Corse en minuscules (2a) est correctement reconnu."""
        response = self.client.get("/city-label/2a004/")
        assert response.status_code == 200
        assert response.json() == "Ajaccio"

    def test_get_city_label_unknown_insee_returns_404(self):
        """Un code INSEE inconnu retourne 404."""
        response = self.client.get("/city-label/99999/")
        assert response.status_code == 404

    def test_get_city_label_invalid_code_returns_404(self):
        """Un code INSEE invalide retourne 404."""
        response = self.client.get("/city-label/0/")
        assert response.status_code == 404
