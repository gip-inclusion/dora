from django.contrib.gis.geos import Point
from django.test import TestCase
from rest_framework.test import APIClient

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import EPCI, City, Department, Region


class SearchViewTests(TestCase):
    """Tests pour l'endpoint /admin-division-search/ (vue search)."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        # Création de données de test pour les villes
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

        # Création de données de test pour les départements
        cls.dept_paris = Department.objects.create(
            code="75",
            name="Paris",
            region="11",
            normalized_name="PARIS",
        )
        cls.dept_rhone = Department.objects.create(
            code="69",
            name="Rhône",
            region="84",
            normalized_name="RHONE",
        )
        cls.dept_corse_sud = Department.objects.create(
            code="2A",
            name="Corse-du-Sud",
            region="94",
            normalized_name="CORSE DU SUD",
        )

        # Création de données de test pour les EPCI
        cls.epci_metropole_lyon = EPCI.objects.create(
            code="200046977",
            name="Métropole de Lyon",
            departments=["69"],
            regions=["84"],
            normalized_name="METROPOLE DE LYON",
        )

        # Création de données de test pour les régions
        cls.region_idf = Region.objects.create(
            code="11",
            name="Île-de-France",
            normalized_name="ILE DE FRANCE",
        )
        cls.region_aura = Region.objects.create(
            code="84",
            name="Auvergne-Rhône-Alpes",
            normalized_name="AUVERGNE RHONE ALPES",
        )

    # -------------------------------------------------------------------------
    # Tests de validation des paramètres
    # -------------------------------------------------------------------------

    def test_search_requires_type_parameter(self):
        response = self.client.get("/admin-division-search/?q=paris")
        assert response.status_code == 400

    def test_search_requires_q_parameter(self):
        response = self.client.get("/admin-division-search/?type=city")
        assert response.status_code == 400

    def test_search_rejects_invalid_type(self):
        response = self.client.get("/admin-division-search/?type=invalid&q=paris")
        assert response.status_code == 400
        assert "type" in response.data
        assert "n'est pas un choix valide" in str(response.data["type"])

    def test_search_empty_query_returns_error(self):
        """Une requête vide doit retourner une erreur."""
        response = self.client.get("/admin-division-search/?type=city&q=")
        assert response.status_code == 400

    # -------------------------------------------------------------------------
    # Tests de recherche de villes (city)
    # -------------------------------------------------------------------------

    def test_search_city_by_name(self):
        response = self.client.get("/admin-division-search/?type=city&q=paris")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "75056"
        assert data[0]["name"] == "Paris"
        assert "similarity" in data[0]

    def test_search_city_by_code(self):
        response = self.client.get("/admin-division-search/?type=city&q=75")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        # La recherche par code doit retourner Paris (code 75056)
        codes = [d["code"] for d in data]
        assert "75056" in codes

    def test_search_city_sorts_by_population(self):
        """Les villes doivent être triées par similarité puis par population."""
        # Créer une autre ville avec "Paris" dans le nom mais moins peuplée
        City.objects.create(
            code="77337",
            name="Paris-sur-Seine",
            department="77",
            epci="",
            region="11",
            postal_codes=["77000"],
            population=1000,
            normalized_name="PARIS SUR SEINE 77",
            center=Point(2.5, 48.5, srid=WGS84),
        )
        response = self.client.get("/admin-division-search/?type=city&q=paris")
        assert response.status_code == 200
        data = response.json()
        # Paris (2M+ habitants) doit apparaître avant Paris-sur-Seine (1000 habitants)
        paris_idx = next(i for i, d in enumerate(data) if d["code"] == "75056")
        paris_sur_seine_idx = next(
            (i for i, d in enumerate(data) if d["code"] == "77337"), len(data)
        )
        assert paris_idx < paris_sur_seine_idx

    # -------------------------------------------------------------------------
    # Tests de recherche de départements (department)
    # -------------------------------------------------------------------------

    def test_search_department_by_name(self):
        response = self.client.get("/admin-division-search/?type=department&q=rhone")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "69"
        assert data[0]["name"] == "Rhône"

    def test_search_department_by_code(self):
        response = self.client.get("/admin-division-search/?type=department&q=69")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "69"

    def test_search_department_corse_2a(self):
        """Test de la recherche du département Corse-du-Sud avec le code 2A."""
        response = self.client.get("/admin-division-search/?type=department&q=2A")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "2A"
        assert data[0]["name"] == "Corse-du-Sud"

    def test_search_department_corse_2b(self):
        """Test de la recherche du département Haute-Corse avec le code 2B."""
        Department.objects.create(
            code="2B",
            name="Haute-Corse",
            region="94",
            normalized_name="HAUTE CORSE",
        )
        response = self.client.get("/admin-division-search/?type=department&q=2B")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "2B"

    # -------------------------------------------------------------------------
    # Tests de recherche d'EPCI
    # -------------------------------------------------------------------------

    def test_search_epci_by_name(self):
        response = self.client.get("/admin-division-search/?type=epci&q=lyon")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "200046977"
        assert "Lyon" in data[0]["name"]

    # -------------------------------------------------------------------------
    # Tests de recherche de régions (region)
    # -------------------------------------------------------------------------

    def test_search_region_by_name(self):
        response = self.client.get(
            "/admin-division-search/?type=region&q=ile de france"
        )
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "11"

    def test_search_region_by_partial_name(self):
        response = self.client.get("/admin-division-search/?type=region&q=auvergne")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert data[0]["code"] == "84"

    # -------------------------------------------------------------------------
    # Tests de comportement général
    # -------------------------------------------------------------------------

    def test_search_returns_max_10_results(self):
        """La recherche doit retourner au maximum 10 résultats."""
        # Créer 15 villes avec des noms similaires
        for i in range(15):
            City.objects.create(
                code=f"99{i:03d}",
                name=f"TestVille{i}",
                department="99",
                epci="",
                region="99",
                postal_codes=[f"99{i:03d}"],
                population=1000 + i,
                normalized_name=f"TESTVILLE{i} 99",
                center=Point(2.0 + i * 0.01, 48.0 + i * 0.01, srid=WGS84),
            )
        response = self.client.get("/admin-division-search/?type=city&q=testville")
        assert response.status_code == 200
        data = response.json()
        assert len(data) <= 10

    def test_search_response_has_no_geom_field(self):
        """La réponse ne doit pas contenir de champ geom."""
        response = self.client.get("/admin-division-search/?type=city&q=paris")
        assert response.status_code == 200
        data = response.json()
        assert len(data) >= 1
        assert "geom" not in data[0]

    def test_search_with_accented_query(self):
        """La recherche doit fonctionner avec des caractères accentués."""
        response = self.client.get("/admin-division-search/?type=region&q=île")
        assert response.status_code == 200
        # La normalisation doit permettre de trouver Île-de-France

    def test_search_is_case_insensitive(self):
        """La recherche doit être insensible à la casse."""
        response_lower = self.client.get("/admin-division-search/?type=city&q=paris")
        response_upper = self.client.get("/admin-division-search/?type=city&q=PARIS")
        response_mixed = self.client.get("/admin-division-search/?type=city&q=PaRiS")

        assert response_lower.status_code == 200
        assert response_upper.status_code == 200
        assert response_mixed.status_code == 200

        # Tous doivent retourner Paris en premier
        assert response_lower.json()[0]["code"] == "75056"
        assert response_upper.json()[0]["code"] == "75056"
        assert response_mixed.json()[0]["code"] == "75056"
