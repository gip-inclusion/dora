from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework.test import APIClient

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import EPCI, City, Department, Region


class ReverseSearchViewTests(TestCase):
    """Tests pour l'endpoint /admin-division-reverse-search/ (vue reverse_search)."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.paris = City.objects.create(
            code="75056",
            name="Paris",
            department="75",
            epci="200054781",
            region="11",
            postal_codes=["75001", "75002"],
            population=2161000,
            normalized_name="PARIS 75",
            center=Point(2.3522, 48.8566, srid=WGS84),
        )
        cls.lyon = City.objects.create(
            code="69123",
            name="Lyon",
            department="69",
            epci="200046977",
            region="84",
            postal_codes=["69001", "69002"],
            population=522969,
            normalized_name="LYON 69",
            center=Point(4.8357, 45.7640, srid=WGS84),
        )
        cls.marseille = City.objects.create(
            code="13055",
            name="Marseille",
            department="13",
            epci="200054807",
            region="93",
            postal_codes=["13001", "13002"],
            population=870731,
            normalized_name="MARSEILLE 13",
            center=Point(5.3698, 43.2965, srid=WGS84),
        )

        Department.objects.create(
            code="75",
            name="Paris",
            region="11",
            normalized_name="PARIS",
        )
        Department.objects.create(
            code="69",
            name="Rhône",
            region="84",
            normalized_name="RHONE",
        )
        Department.objects.create(
            code="13",
            name="Bouches-du-Rhône",
            region="93",
            normalized_name="BOUCHES DU RHONE",
        )

        EPCI.objects.create(
            code="200054781",
            name="Paris Métropole",
            departments=["75"],
            regions=["11"],
            normalized_name="PARIS METROPOLE",
        )
        EPCI.objects.create(
            code="200046977",
            name="Métropole de Lyon",
            departments=["69"],
            regions=["84"],
            normalized_name="METROPOLE DE LYON",
        )

        Region.objects.create(
            code="11",
            name="Île-de-France",
            normalized_name="ILE DE FRANCE",
        )
        Region.objects.create(
            code="84",
            name="Auvergne-Rhône-Alpes",
            normalized_name="AUVERGNE RHONE ALPES",
        )
        Region.objects.create(
            code="93",
            name="Provence-Alpes-Côte d'Azur",
            normalized_name="PROVENCE ALPES COTE D AZUR",
        )

    # -------------------------------------------------------------------------
    # Validation des paramètres
    # -------------------------------------------------------------------------

    def test_requires_type_parameter(self):
        response = self.client.get(
            "/admin-division-reverse-search/?lat=48.8566&lon=2.3522"
        )
        assert response.status_code == 400
        assert "type" in response.json()

    def test_requires_lat_parameter(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lon=2.3522"
        )
        assert response.status_code == 400
        assert "lat" in response.json()

    def test_requires_lon_parameter(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=48.8566"
        )
        assert response.status_code == 400
        assert "lon" in response.json()

    def test_rejects_invalid_type(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=invalid&lat=48.8566&lon=2.3522"
        )
        assert response.status_code == 400
        data = response.json()
        assert "type" in data

    def test_rejects_invalid_lat(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=not_a_number&lon=2.3522"
        )
        assert response.status_code == 400
        assert "lat" in response.json()

    def test_rejects_invalid_lon(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=48.8566&lon=not_a_number"
        )
        assert response.status_code == 400
        assert "lon" in response.json()

    # -------------------------------------------------------------------------
    # Recherche par type=city (plus proche centre)
    # -------------------------------------------------------------------------

    def test_reverse_search_city_paris(self):
        """Coordonnées exactes du centre de Paris (fixture) → Paris."""
        lat, lon = self.paris.center.y, self.paris.center.x
        response = self.client.get(
            f"/admin-division-reverse-search/?type=city&lat={lat}&lon={lon}"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "75056"
        assert data["name"] == "Paris"
        assert set(data.keys()) == {"code", "name"}

    def test_reverse_search_city_lyon(self):
        """Coordonnées proches de Lyon (pas le centre exact) → Lyon (ville la plus proche)."""
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=45.77&lon=4.84"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "69123"
        assert data["name"] == "Lyon"

    def test_reverse_search_city_marseille(self):
        """Coordonnées proches de Marseille (pas le centre exact) → Marseille (ville la plus proche)."""
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=43.30&lon=5.37"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "13055"
        assert data["name"] == "Marseille"

    def test_reverse_search_city_dijon(self):
        """Coordonnées de Dijon (hors fixtures) → Lyon (ville la plus proche)."""
        response = self.client.get(
            "/admin-division-reverse-search/?type=city&lat=47.322&lon=5.0415"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "69123"
        assert data["name"] == "Lyon"
        assert set(data.keys()) == {"code", "name"}

    # -------------------------------------------------------------------------
    # Recherche par type=department
    # -------------------------------------------------------------------------

    def test_reverse_search_department_from_paris(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=department&lat=48.8566&lon=2.3522"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "75"
        assert data["name"] == "Paris"

    def test_reverse_search_department_from_lyon(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=department&lat=45.7640&lon=4.8357"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "69"
        assert data["name"] == "Rhône"

    # -------------------------------------------------------------------------
    # Recherche par type=epci
    # -------------------------------------------------------------------------

    def test_reverse_search_epci_from_lyon(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=epci&lat=45.7640&lon=4.8357"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "200046977"
        assert data["name"] == "Métropole de Lyon"

    def test_reverse_search_epci_from_paris(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=epci&lat=48.8566&lon=2.3522"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "200054781"
        assert data["name"] == "Paris Métropole"

    # -------------------------------------------------------------------------
    # Recherche par type=region
    # -------------------------------------------------------------------------

    def test_reverse_search_region_from_paris(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=region&lat=48.8566&lon=2.3522"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "11"
        assert data["name"] == "Île-de-France"

    def test_reverse_search_region_from_lyon(self):
        response = self.client.get(
            "/admin-division-reverse-search/?type=region&lat=45.7640&lon=4.8357"
        )
        assert response.status_code == 200
        data = response.json()
        assert data["code"] == "84"
        assert data["name"] == "Auvergne-Rhône-Alpes"
