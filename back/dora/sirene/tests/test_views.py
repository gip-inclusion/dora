from model_bakery import baker
from rest_framework.test import APITestCase


class SearchSireneTestCase(APITestCase):
    def test_missing_q_returns_400(self):
        response = self.client.get("/search-sirene/75056/")

        assert response.status_code == 400

    def test_empty_q_returns_400(self):
        response = self.client.get("/search-sirene/75056/?q=")

        assert response.status_code == 400

    def test_returns_matches(self):
        baker.make(
            "sirene.Establishment",
            siret="12345678900011",
            siren="123456789",
            name="ASSOCIATION SOLIDARITE",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="33063",
            is_siege=True,
            full_search_text="ASSOCIATION SOLIDARITE",
        )
        baker.make(
            "sirene.Establishment",
            siret="98765432100012",
            siren="987654321",
            name="BOULANGERIE DUPONT",
            parent_name="BOULANGERIE DUPONT",
            city_code="33063",
            is_siege=True,
            full_search_text="BOULANGERIE DUPONT",
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        sirets = [item["siret"] for item in response.json()]
        assert "12345678900011" in sirets
        assert "98765432100012" not in sirets

    def test_filters_by_citycode(self):
        baker.make(
            "sirene.Establishment",
            siret="11111111100011",
            siren="111111111",
            name="ASSOCIATION SOLIDARITE",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="75056",
            is_siege=True,
            full_search_text="ASSOCIATION SOLIDARITE",
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        assert response.json() == []

    def test_excludes_obsolete_structures(self):
        baker.make(
            "sirene.Establishment",
            siret="22222222200011",
            siren="222222222",
            name="ASSOCIATION SOLIDARITE",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="33063",
            is_siege=True,
            full_search_text="ASSOCIATION SOLIDARITE",
        )
        baker.make(
            "structures.Structure",
            siret="22222222200011",
            is_obsolete=True,
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        assert response.json() == []

    def test_excludes_nd_name(self):
        baker.make(
            "sirene.Establishment",
            siret="33333333300011",
            siren="333333333",
            name="[ND]",
            parent_name="[ND]",
            city_code="33063",
            is_siege=True,
            full_search_text="SOLIDARITE",
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        assert response.json() == []

    def test_excludes_empty_name_when_not_siege(self):
        baker.make(
            "sirene.Establishment",
            siret="44444444400011",
            siren="444444444",
            name="",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="33063",
            is_siege=False,
            full_search_text="ASSOCIATION SOLIDARITE",
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        assert response.json() == []

    def test_keeps_empty_name_when_siege(self):
        baker.make(
            "sirene.Establishment",
            siret="55555555500011",
            siren="555555555",
            name="",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="33063",
            is_siege=True,
            full_search_text="ASSOCIATION SOLIDARITE",
        )

        response = self.client.get("/search-sirene/33063/?q=solidarite")

        assert response.status_code == 200
        sirets = [item["siret"] for item in response.json()]
        assert "55555555500011" in sirets

    def test_normalizes_accents(self):
        baker.make(
            "sirene.Establishment",
            siret="66666666600011",
            siren="666666666",
            name="ASSOCIATION SOLIDARITE",
            parent_name="ASSOCIATION SOLIDARITE",
            city_code="33063",
            is_siege=True,
            full_search_text="ASSOCIATION SOLIDARITE",
        )

        response = self.client.get("/search-sirene/33063/?q=Solidarité")

        assert response.status_code == 200
        sirets = [item["siret"] for item in response.json()]
        assert "66666666600011" in sirets
