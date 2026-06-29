import random
from unittest import mock

import pytest
import requests
from django.contrib.gis.geos import Point
from django.urls import reverse
from model_bakery import baker
from rest_framework.exceptions import ValidationError

from dora.core.constants import WGS84
from dora.core.test_utils import (
    make_published_service,
    make_service,
    make_structure,
    make_user,
)
from dora.data_inclusion.test_utils import FakeDataInclusionClient, make_di_service_data
from dora.decoupage_administratif.models import AdminDivisionType, City
from dora.services.enums import ServiceStatus
from dora.services.search import MAX_DISTANCE
from dora.services.serializers import SearchKeywordSerializer
from dora.services.views import _validate_search_categories_and_subcategories


@pytest.fixture
def city():
    return baker.make(
        "decoupage_administratif.City",
        department="01",
        epci="200000000",
        region="11",
    )


@pytest.fixture
def orphan_service():
    # service devant sortir lors d'une recherche globale
    service = make_service(
        status=ServiceStatus.PUBLISHED,
        diffusion_zone_type=AdminDivisionType.COUNTRY,
        # le résultat de `make_service` est maintenant rattaché à une structure "non-orpheline"
        # mais on veut ici un service "orphelin" par défaut
        structure=make_structure(),
    )
    return service


@pytest.fixture
def structure_with_user():
    return make_structure(user=make_user())


def test_search_services_with_obsolete_structure(api_client, city):
    # les services rattachés à une structure obsolète
    # doivent être filtrés lors de la recherche

    # Service publié avec structure non obsolète
    service = make_published_service(diffusion_zone_type=AdminDivisionType.COUNTRY)

    fake_di_client = FakeDataInclusionClient()

    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}")

    assert response.status_code == 200
    assert response.data["services"], (
        "un service devrait être retourné (structure non obsolète)"
    )

    [found] = response.data["services"]

    assert found["slug"] == service.slug

    # on rend la structure obsolète
    service.structure.is_obsolete = True
    service.structure.save()

    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}")

    assert response.status_code == 200
    assert not response.data["services"], (
        "aucun service ne devrait être retourné (structure obsolète)"
    )


def test_search_services_with_orphan_structure(
    api_client, orphan_service, structure_with_user, city
):
    # les services rattachés à une structure orpheline
    # doivent être filtrés lors de la recherche

    fake_di_client = FakeDataInclusionClient()

    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}")

    assert response.status_code == 200
    assert not response.data["services"], (
        "aucun service ne devrait être retourné (structure orpheline)"
    )

    # on ajoute une structure avec un utilisateur au service
    orphan_service.structure = structure_with_user
    orphan_service.save()

    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}")

    assert response.status_code == 200
    assert response.data["services"], (
        "un service devrait être retourné (structure avec utilisateur)"
    )

    [found] = response.data["services"]

    assert found["slug"] == orphan_service.slug


def test_search_services_includes_thematiques_empty_list(api_client, city):
    # Un service service DI ayant le champ thematiques avec une liste vide doit être retourné

    with mock.patch("dora.data_inclusion.di_client_factory") as mock_di_client_factory:
        di_client = FakeDataInclusionClient()
        service = make_di_service_data(zone_eligibilite=[city.code], thematiques=[])
        di_client.services.append(service)

        mock_di_client_factory.return_value = di_client

        response = api_client.get(f"/search/?city={city.code}")

        assert response.status_code == 200

        assert len(response.data["services"]) == 1, "un service devrait être retourné"


def test_search_services_includes_thematiques_null(api_client, city):
    # Un service service DI ayant le champ thematiques à null doit être retourné

    with mock.patch("dora.data_inclusion.di_client_factory") as mock_di_client_factory:
        di_client = FakeDataInclusionClient()
        service = make_di_service_data(zone_eligibilite=[city.code], thematiques=None)
        di_client.services.append(service)

        mock_di_client_factory.return_value = di_client

        response = api_client.get(f"/search/?city={city.code}")

        assert response.status_code == 200

        assert len(response.data["services"]) == 1, "un service devrait être retourné"


class TestValidateSearchCategoriesAndSubcategories:
    """Teste la validation des catégories et sous-catégories de la recherche."""

    def test_validate_invalid_categories(self):
        """Teste que les catégories invalides sont rejetées."""
        baker.make("ServiceCategory", value="cat1", label="Catégorie 1")

        with pytest.raises(ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=["invalid_cat"], subcategories_list=None
            )

        assert "Catégories invalides" in str(exc_info.value)

    def test_validate_invalid_subcategories(self):
        """Teste que les sous-catégories invalides sont rejetées."""
        baker.make("ServiceSubCategory", value="cat1--sub1", label="Sous-catégorie 1")

        with pytest.raises(ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=None, subcategories_list=["invalid--sub"]
            )

        assert "Sous-catégories invalides" in str(exc_info.value)

    def test_validate_obsolete_categories(self):
        """Teste que les catégories obsolètes sont rejetées."""
        baker.make(
            "ServiceCategory",
            value="obsolete_cat",
            label="Catégorie obsolète",
            is_obsolete=True,
        )

        with pytest.raises(ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=["obsolete_cat"], subcategories_list=None
            )

        assert "Catégories invalides" in str(exc_info.value)

    def test_validate_obsolete_subcategories(self):
        """Teste que les sous-catégories obsolètes sont rejetées."""
        baker.make(
            "ServiceSubCategory",
            value="cat1--obsolete_sub",
            label="Sous-catégorie obsolète",
            is_obsolete=True,
        )

        with pytest.raises(ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=None, subcategories_list=["cat1--obsolete_sub"]
            )

        assert "Sous-catégories invalides" in str(exc_info.value)


def test_search_endpoint_rejects_invalid_categories(api_client, city):
    """Teste que le endpoint de recherche rejette les catégories invalides."""
    baker.make("ServiceCategory", value="cat1", label="Catégorie 1")

    fake_di_client = FakeDataInclusionClient()
    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}&cats=invalid_cat")

    assert response.status_code == 400
    # L'exception handler retourne une liste avec code et message
    assert isinstance(response.data, list)
    assert len(response.data) > 0
    assert "message" in response.data[0]
    assert "Catégories invalides" in str(response.data[0]["message"])


def test_search_endpoint_rejects_invalid_subcategories(api_client, city):
    """Teste que le endpoint de recherche rejette les sous-catégories invalides."""
    baker.make("ServiceSubCategory", value="cat1--sub1", label="Sous-catégorie 1")

    fake_di_client = FakeDataInclusionClient()
    with mock.patch(
        "dora.data_inclusion.di_client_factory", return_value=fake_di_client
    ):
        response = api_client.get(f"/search/?city={city.code}&subs=invalid--sub")

    assert response.status_code == 400
    # L'exception handler retourne une liste avec code et message
    assert isinstance(response.data, list)
    assert len(response.data) > 0
    assert "message" in response.data[0]
    assert "Sous-catégories invalides" in str(response.data[0]["message"])


class TestSearchKeyword:
    @property
    def api_result(self):
        return {
            "service": {
                "source": "emplois-de-linclusion",
                "structure_id": "dora--42",
                "id": "emplois-de-linclusion--17",
                "nom": "Atelier insertion et posture professionnelle",
                "description": "Cet atelier-conseil vous permet d’identifier les compétences à développer pour atteindre vos objectifs d’évolution professionnelle et à découvrir les différentes modalités de formation.  Durée d’une journée et inscription via votre espace France Travail.",
                "lien_source": "https://dora.inclusion.beta.gouv.fr/services/ass-pour-droit-a-l-i-nhes",
                "date_maj": "2025-02-14",
                "type": "accompagnement",
                "thematiques": ["numerique--acquerir-un-equipement"],
                "frais": "gratuit",
                "frais_precisions": "10€ pour l’adhésion annuelle",
                "publics": ["femmes"],
                "publics_precisions": "Le jeune entre 15 et 18 ans.",
                "conditions_acces": "Maîtrise de la langue française à l’oral et à l’écrit",
                "commune": "string",
                "code_postal": "64531",
                "code_insee": "CiXXQ",
                "adresse": "string",
                "complement_adresse": "string",
                "longitude": 0,
                "latitude": 0,
                "telephone": "+33123456789",
                "courriel": "exemple@inclusion.gouv.fr",
                "modes_accueil": ["a-distance"],
                "zone_eligibilite": ["75056"],
                "contact_nom_prenom": "string",
                "lien_mobilisation": "https://www.actionlogement.fr/demande-cfi",
                "modes_mobilisation": ["envoyer-un-courriel"],
                "mobilisable_par": ["professionnels"],
                "mobilisation_precisions": "La demande est à faire depuis l’espace personnel du demandeur d’emploi, rubrique « mes aides », formulaire spécifique « Aide à la mobilité ».",
                "volume_horaire_hebdomadaire": 1,
                "nombre_semaines": 3,
                "horaires_accueil": "Mo-Fr 08:30-12:30; PH off",
                "adresse_certifiee": True,
                "score_qualite": 1,
                "structure": {
                    "source": "emplois-de-linclusion",
                    "id": "emplois-de-linclusion--17",
                    "nom": "Centre social Le Tournesol",
                    "date_maj": "2025-02-14",
                    "description": "L’association 3027 offre un accès gratuit aux arts, à la culture et au sport pour toutes et tous sans distinction et en priorité aux personnes en situation de précarité et d’isolement.",
                    "lien_source": "https://dora.inclusion.beta.gouv.fr/structures/ass-pour-droit-a-l-i-nhes",
                    "siret": "13003013300016",
                    "commune": "string",
                    "code_postal": "93217",
                    "code_insee": "WsazB",
                    "adresse": "string",
                    "complement_adresse": "string",
                    "longitude": 0,
                    "latitude": 0,
                    "telephone": "+33123456789",
                    "courriel": "exemple@inclusion.gouv.fr",
                    "site_web": "https://example.com/",
                    "horaires_accueil": "Mo-Fr 08:30-12:30; PH off",
                    "accessibilite_lieu": "https://acceslibre.beta.gouv.fr/app/17-la-greve-sur-mignon/a/mairie/erp/mairie-la-greve-sur-mignon/",
                    "reseaux_porteurs": ["mission-locale"],
                    "adresse_certifiee": True,
                },
            },
            "distance": 0,
            "score_recherche": 0,
        }

    @pytest.mark.parametrize(
        "params,expected",
        [
            pytest.param(
                {},
                {
                    "nonFieldErrors": [
                        {
                            "message": "Au moins un champ doit être fourni, parmi q, code_commune, code_departement, code_region, lon, lat.",
                            "code": "invalid",
                        }
                    ]
                },
                id="noquery",
            ),
            pytest.param(
                {f: "" for f in set(SearchKeywordSerializer().fields) - {"locs"}},
                {
                    "nonFieldErrors": [
                        {
                            "message": "Au moins un champ doit être fourni, parmi q, code_commune, code_departement, code_region, lon, lat.",
                            "code": "invalid",
                        }
                    ]
                },
                id="empty",
            ),
            pytest.param(
                {"lat": "12.1234"},
                {
                    "nonFieldErrors": [
                        {
                            "message": "Le champ lon est requis lorsque lat est fourni.",
                            "code": "invalid",
                        }
                    ]
                },
                id="lat",
            ),
            pytest.param(
                {"lon": "12.1234"},
                {
                    "nonFieldErrors": [
                        {
                            "message": "Le champ lat est requis lorsque lon est fourni.",
                            "code": "invalid",
                        }
                    ]
                },
                id="lon",
            ),
            pytest.param(
                {"lat": "12.1234", "q": "foo"},
                {
                    "nonFieldErrors": [
                        {
                            "message": "Le champ lon est requis lorsque lat est fourni.",
                            "code": "invalid",
                        }
                    ]
                },
                id="lat_with_q",
            ),
        ],
    )
    def test_invalid_payload(self, api_client, params, expected):
        response = api_client.get(reverse("search-keyword"), params)
        assert response.status_code == 400
        assert response.json() == expected

    @pytest.mark.parametrize(
        "services_kwargs,expected_coords",
        [
            pytest.param(
                [{"geom": Point(-0.123, 0.123, srid=WGS84)}],
                [-0.123, 0.123],
                id="single",
            ),
            pytest.param(
                [
                    {"geom": Point(-1, 1, srid=WGS84)},
                    {"geom": Point(-2, 2, srid=WGS84)},
                ],
                [-1.5, 1.5],
                id="search_center_average",
            ),
        ],
    )
    def test_search_api(self, api_client, expected_coords, services_kwargs):
        results = []
        expected_slugs = []
        for i, service_kwargs in enumerate(services_kwargs):
            service = make_published_service(
                diffusion_zone_type=AdminDivisionType.COUNTRY,
                **service_kwargs,
            )
            result = self.api_result
            result["service"]["id"] = f"dora--{service.pk}"
            result["service"]["source"] = "dora"
            # La distance est ignorée dans le tri.
            result["distance"] = random.uniform(0, 10)
            result["score_recherche"] = 0.1 * i
            results.append(result)
            expected_slugs.insert(0, service.slug)
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=FakeDataInclusionClient(services=results),
        ):
            response = api_client.get(reverse("search-keyword"), {"q": "foo"})

        assert response.status_code == 200
        response_json = response.json()
        assert [s["slug"] for s in response_json["services"]] == expected_slugs
        assert response_json["searchCenter"] == expected_coords

    def test_search_city(self, api_client):
        paris = City.objects.create(
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
        service = make_published_service(diffusion_zone_type=AdminDivisionType.COUNTRY)
        result = self.api_result
        result["service"]["id"] = f"dora--{service.pk}"
        result["service"]["source"] = "dora"
        result["service"]["code_postal"] = paris.postal_codes[0]
        result["service"]["code_insee"] = paris.code
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=FakeDataInclusionClient(services=[result]),
        ):
            response = api_client.get(
                reverse("search-keyword"), {"code_commune": paris.code}
            )

        assert response.status_code == 200
        response_json = response.json()
        assert [s["slug"] for s in response_json["services"]] == [service.slug]
        assert response_json["searchCenter"] == [paris.center.x, paris.center.y]

    def test_search_lat_lon_0(self, api_client):
        service = make_published_service(diffusion_zone_type=AdminDivisionType.COUNTRY)
        result = self.api_result
        result["service"]["id"] = f"dora--{service.pk}"
        result["service"]["source"] = "dora"
        result["service"]["latitude"] = 0
        result["service"]["longitude"] = 0
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=FakeDataInclusionClient(services=[result]),
        ):
            response = api_client.get(reverse("search-keyword"), {"lat": 0, "lon": 0})

        assert response.status_code == 200
        response_json = response.json()
        assert [s["slug"] for s in response_json["services"]] == [service.slug]
        assert response_json["searchCenter"] == [0, 0]

    def test_di_unavailable(self, api_client):
        def requests_error(*args, **kwargs):
            raise requests.HTTPError()

        fake_client = FakeDataInclusionClient()
        fake_client.search = requests_error
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=fake_client,
        ):
            response = api_client.get(reverse("search-keyword"), {"q": "foo"})

        assert response.status_code == 503
        assert response.json() == {
            "detail": {
                "message": (
                    "L’API data.inclusion.gouv.fr nécessaire pour la recherche, "
                    "n’est pas disponible. Merci de réessayer ultérieurement."
                ),
                "code": "service_unavailable",
            }
        }

    @pytest.mark.parametrize(
        "distance",
        [
            pytest.param(3.0, id="3km"),
            pytest.param(MAX_DISTANCE + 1, id="max-distance"),
            pytest.param(None, id="None"),
        ],
    )
    def test_search_api_di_result(self, api_client, distance):
        results = [
            {
                "distance": distance,
                "score_recherche": 0.69,
                "service": {
                    "adresse": "Avenue Jeanne d'Arc",
                    "adresse_certifiee": True,
                    "code_insee": "33268",
                    "code_postal": "33460",
                    "commune": "Margaux-Cantenac",
                    "complement_adresse": "Salle annexe",
                    "conditions_acces": "Accessible facilement.",
                    "date_maj": "2025-11-26",
                    "description": "L’oiseau lire",
                    "frais": "payant",
                    "frais_precisions": "Une participation financière de 3 €.",
                    "horaires_accueil": "Mo 13:00-16:00 open, Tu 13:00-18:00 open, We "
                    "closed, Th 14:00-16:00 open, Fr closed, Sa "
                    "closed, Su closed",
                    "id": "soliguide--id",
                    "latitude": 42,
                    "lien_mobilisation": None,
                    "lien_source": "https://soliguide.fr/fr/fiche/loiseau-lire-38963",
                    "longitude": -42,
                    "mobilisable_par": ["usagers", "professionnels"],
                    "mobilisation_precisions": "",
                    "modes_accueil": ["en-presentiel"],
                    "modes_mobilisation": ["telephoner", "envoyer-un-courriel"],
                    "nom": "Cours de français",
                    "nombre_semaines": None,
                    "publics": ["tous-publics"],
                    "publics_precisions": None,
                    "score_qualite": 0.99,
                    "source": "soliguide",
                    "structure": {
                        "accessibilite_lieu": None,
                        "adresse": "Avenue Jeanne d'Arc",
                        "adresse_certifiee": True,
                        "code_insee": "33268",
                        "code_postal": "33460",
                        "commune": "Margaux-Cantenac",
                        "complement_adresse": "Salle annexe Espace Ginestet",
                        "courriel": "contact@oiseaulire33.fr",
                        "date_maj": "2025-11-26",
                        "description": "L'Oiseau Lire",
                        "horaires_accueil": "Mo 13:00-16:00 open, Tu "
                        "13:00-18:00 open, We closed, "
                        "Th 14:00-16:00 open, Fr "
                        "closed, Sa closed, Su closed",
                        "id": "soliguide--38963",
                        "latitude": 45.040763,
                        "lien_source": "https://soliguide.fr/fr/fiche/loiseau-lire-38963",
                        "longitude": -0.67778,
                        "nom": "L'Oiseau Lire",
                        "reseaux_porteurs": None,
                        "siret": None,
                        "site_web": None,
                        "source": "soliguide",
                        "telephone": "+33632898444",
                    },
                    "structure_id": "soliguide--38963",
                    "telephone": "+33632898444",
                    "thematiques": ["lecture-ecriture-calcul--maitriser-le-francais"],
                    "type": "formation",
                    "volume_horaire_hebdomadaire": None,
                    "zone_eligibilite": ["33"],
                },
            }
        ]
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=FakeDataInclusionClient(services=results),
        ):
            response = api_client.get(reverse("search-keyword"), {"q": "oiseau"})

        assert response.status_code == 200
        response_json = response.json()
        assert [s["slug"] for s in response_json["services"]] == ["soliguide--id"]
        assert response_json["searchCenter"] == [-42, 42]

    def test_search_api_di_result_distance_none(self, api_client):
        results = [
            {
                "distance": 3.0,
                "score_recherche": 0.69,
                "service": {
                    "adresse": "Avenue Jeanne d'Arc",
                    "adresse_certifiee": True,
                    "code_insee": "33268",
                    "code_postal": "33460",
                    "commune": "Margaux-Cantenac",
                    "complement_adresse": "Salle annexe",
                    "conditions_acces": "Accessible facilement.",
                    "date_maj": "2025-11-26",
                    "description": "L’oiseau lire",
                    "frais": "payant",
                    "frais_precisions": "Une participation financière de 3 €.",
                    "horaires_accueil": "Mo 13:00-16:00 open, Tu 13:00-18:00 open, We "
                    "closed, Th 14:00-16:00 open, Fr closed, Sa "
                    "closed, Su closed",
                    "id": "soliguide--id",
                    "latitude": 42,
                    "lien_mobilisation": None,
                    "lien_source": "https://soliguide.fr/fr/fiche/loiseau-lire-38963",
                    "longitude": -42,
                    "mobilisable_par": ["usagers", "professionnels"],
                    "mobilisation_precisions": "",
                    "modes_accueil": ["en-presentiel"],
                    "modes_mobilisation": ["telephoner", "envoyer-un-courriel"],
                    "nom": "Cours de français",
                    "nombre_semaines": None,
                    "publics": ["tous-publics"],
                    "publics_precisions": None,
                    "score_qualite": 0.99,
                    "source": "soliguide",
                    "structure": {
                        "accessibilite_lieu": None,
                        "adresse": "Avenue Jeanne d'Arc",
                        "adresse_certifiee": True,
                        "code_insee": "33268",
                        "code_postal": "33460",
                        "commune": "Margaux-Cantenac",
                        "complement_adresse": "Salle annexe Espace Ginestet",
                        "courriel": "contact@oiseaulire33.fr",
                        "date_maj": "2025-11-26",
                        "description": "L'Oiseau Lire",
                        "horaires_accueil": "Mo 13:00-16:00 open, Tu "
                        "13:00-18:00 open, We closed, "
                        "Th 14:00-16:00 open, Fr "
                        "closed, Sa closed, Su closed",
                        "id": "soliguide--38963",
                        "latitude": 45.040763,
                        "lien_source": "https://soliguide.fr/fr/fiche/loiseau-lire-38963",
                        "longitude": -0.67778,
                        "nom": "L'Oiseau Lire",
                        "reseaux_porteurs": None,
                        "siret": None,
                        "site_web": None,
                        "source": "soliguide",
                        "telephone": "+33632898444",
                    },
                    "structure_id": "soliguide--38963",
                    "telephone": "+33632898444",
                    "thematiques": ["lecture-ecriture-calcul--maitriser-le-francais"],
                    "type": "formation",
                    "volume_horaire_hebdomadaire": None,
                    "zone_eligibilite": ["33"],
                },
            }
        ]
        with mock.patch(
            "dora.data_inclusion.di_client_factory",
            return_value=FakeDataInclusionClient(services=results),
        ):
            response = api_client.get(reverse("search-keyword"), {"q": "oiseau"})

        assert response.status_code == 200
        response_json = response.json()
        assert [s["slug"] for s in response_json["services"]] == ["soliguide--id"]
        assert response_json["searchCenter"] == [-42, 42]
