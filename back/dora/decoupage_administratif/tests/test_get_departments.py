from django.test import TestCase
from rest_framework.test import APIClient

from dora.decoupage_administratif.models import Department


class GetDepartmentsViewTests(TestCase):
    """Tests pour l'endpoint /admin-division-departments/ (vue get_departments)."""

    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.dept_75 = Department.objects.create(
            code="75",
            name="Paris",
            region="11",
            normalized_name="PARIS",
        )
        cls.dept_69 = Department.objects.create(
            code="69",
            name="Rhône",
            region="84",
            normalized_name="RHONE",
        )
        cls.dept_2a = Department.objects.create(
            code="2A",
            name="Corse-du-Sud",
            region="94",
            normalized_name="CORSE DU SUD",
        )

    def test_get_departments_without_param_returns_all_sorted_by_code(self):
        """Sans dept_codes, tous les départements sont retournés, triés par code."""
        response = self.client.get("/admin-division-departments/")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3
        assert [d["code"] for d in data] == ["2A", "69", "75"]
        assert data[0]["name"] == "Corse-du-Sud"
        assert data[1]["name"] == "Rhône"
        assert data[2]["name"] == "Paris"

    def test_get_departments_with_single_code(self):
        """Avec dept_codes=75, seul le département Paris est retourné."""
        response = self.client.get("/admin-division-departments/?dept_codes=75")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["code"] == "75"
        assert data[0]["name"] == "Paris"

    def test_get_departments_with_multiple_codes_returns_sorted_by_code(self):
        """Avec plusieurs codes, les départements sont triés par code."""
        response = self.client.get("/admin-division-departments/?dept_codes=75,69")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 2
        assert [d["code"] for d in data] == ["69", "75"]

    def test_get_departments_with_corse_code_2a(self):
        """Le code 2A (Corse-du-Sud) est correctement récupéré."""
        response = self.client.get("/admin-division-departments/?dept_codes=2A")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["code"] == "2A"
        assert data[0]["name"] == "Corse-du-Sud"

    def test_get_departments_response_has_code_and_name(self):
        """Chaque élément de la réponse contient code et name."""
        response = self.client.get("/admin-division-departments/?dept_codes=69")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert "code" in data[0]
        assert "name" in data[0]
        assert data[0]["code"] == "69"
        assert data[0]["name"] == "Rhône"

    def test_get_departments_empty_param_returns_all(self):
        """dept_codes vide est traité comme l'absence de paramètre."""
        response = self.client.get("/admin-division-departments/?dept_codes=")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 3

    def test_get_departments_unknown_codes_return_only_matching(self):
        """Les codes inconnus sont ignorés ; seuls les départements trouvés sont retournés."""
        response = self.client.get("/admin-division-departments/?dept_codes=75,99")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 1
        assert data[0]["code"] == "75"
        assert data[0]["name"] == "Paris"
