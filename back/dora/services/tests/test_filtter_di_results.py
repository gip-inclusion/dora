from model_bakery import baker
from rest_framework.test import APITestCase

from dora.services.search import _filter_di_results


class FilterDiResultsTestCase(APITestCase):
    def setUp(self):
        self.raw_di_results = [
            {
                "distance": 0,
                "service": {
                    "id": "mediation-numerique--1",
                    "source": "mediation-numerique",
                    "nom": "Service médiation numérique Coop numérique",
                    "structure": {
                        "id": "mediation-numerique--Coop_numérique_123",
                    },
                },
            },
            {
                "distance": 0,
                "service": {
                    "id": "mediation-numerique--2",
                    "source": "mediation-numerique",
                    "nom": "Service médiation numérique France Services",
                    "structure": {
                        "id": "mediation-numerique--France-Services_456",
                    },
                },
            },
            {
                "distance": 0,
                "service": {
                    "id": "emplois-de-linclusion--1",
                    "source": "emplois-de-linclusion",
                    "nom": "Service emplois",
                    "structure": {
                        "id": "emplois-de-linclusion--123",
                    },
                },
            },
        ]

    def test_filter_excludes_mediation_numerique_for_vosges(self):
        """Test que les services mediation-numerique sont exclus pour les Vosges."""
        commune_vosges = baker.make(
            "decoupage_administratif.Commune",
            code="88000",
            code_departement="88",
        )
        filtered = _filter_di_results(self.raw_di_results, commune_vosges.code)
        assert len(filtered) == 1
        assert filtered[0]["service"]["source"] == "emplois-de-linclusion"

    def test_filter_excludes_mediation_numerique_but_keeps_france_services_for_somme(
        self,
    ):
        """Test que les services mediation-numerique sont exclus pour la Somme,
        mais que les services France Services sont conservés.
        """
        commune_somme = baker.make(
            "decoupage_administratif.Commune",
            code="80000",
            code_departement="80",
        )
        filtered = _filter_di_results(self.raw_di_results, commune_somme.code)
        assert len(filtered) == 2
        assert filtered[0]["service"]["source"] == "mediation-numerique"
        assert (
            filtered[0]["service"]["structure"]["id"]
            == "mediation-numerique--France-Services_456"
        )
        assert filtered[1]["service"]["source"] == "emplois-de-linclusion"

    def test_filter_returns_all_results_for_other_departments(self):
        """Test que tous les résultats sont retournés pour les autres départements."""
        commune = baker.make(
            "decoupage_administratif.Commune",
            code="75001",
            code_departement="75",
        )

        filtered = _filter_di_results(self.raw_di_results, commune.code)

        assert len(filtered) == 3
        assert filtered == self.raw_di_results

    def test_filter_returns_all_results_when_commune_not_found(self):
        """Test que tous les résultats sont retournés si la commune n'existe pas."""
        filtered = _filter_di_results(self.raw_di_results, "99999")

        assert len(filtered) == 3
        assert filtered == self.raw_di_results
