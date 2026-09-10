import pytest
from django.contrib.gis.geos import Point

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import EPCI, City

URL = "/admin-division-search-epcis-cities/"


def make_city(code, name, normalized_name=None, population=1000, department="69"):
    return City.objects.create(
        code=code,
        name=name,
        normalized_name=normalized_name or name.upper(),
        department=department,
        epci="",
        region="84",
        postal_codes=[],
        population=population,
        center=Point(4.8, 45.7, srid=WGS84),
    )


def make_epci(code, name, normalized_name=None, departments=None):
    return EPCI.objects.create(
        code=code,
        name=name,
        normalized_name=normalized_name or name.upper(),
        departments=departments or ["69"],
        regions=["84"],
    )


@pytest.fixture
def territories():
    make_city("69123", "Lyon", population=522969)
    make_city("13055", "Marseille", population=870731, department="13")
    make_epci("200046977", "Métropole de Lyon", "METROPOLE DE LYON")
    make_epci("200070340", "CC des Deux Rives", "CC DES DEUX RIVES", ["45", "89"])


@pytest.mark.parametrize(
    "query,group,expected",
    [
        pytest.param(
            "Lyon",
            "cities",
            {"label": "Lyon", "value": "69123"},
            id="commune-par-nom",
        ),
        pytest.param(
            "Deux Rives",
            "epcis",
            {"label": "CC des Deux Rives", "value": "200070340"},
            id="epci-par-nom",
        ),
        pytest.param(
            "200070340",
            "epcis",
            {"label": "CC des Deux Rives", "value": "200070340"},
            id="epci-par-code",
        ),
    ],
)
def test_search_returns_the_matching_territory(
    api_client, territories, query, group, expected
):
    response = api_client.get(URL, {"q": query})
    assert response.status_code == 200
    assert expected in response.json()[group]


def test_search_returns_nothing_without_a_match(api_client, territories):
    response = api_client.get(URL, {"q": "Zzzzzzzz"})
    assert response.status_code == 200
    assert response.json() == {"cities": [], "epcis": []}


def test_search_requires_a_query(api_client):
    response = api_client.get(URL)
    assert response.status_code == 400


def test_search_caps_the_total_number_of_results(api_client, territories):
    for i in range(8):
        make_city(f"6900{i}", f"Lyonnet {i}", population=1000 - i)
        make_epci(f"20000000{i}", f"CC Lyonnaise {i}")

    response = api_client.get(URL, {"q": "Lyon"})

    assert response.status_code == 200
    data = response.json()
    assert len(data["cities"]) + len(data["epcis"]) == 10


def test_search_ranks_an_epci_code_match_above_name_matches(api_client, territories):
    """Une correspondance sur le code d'un EPCI ne doit rien à son nom : sa
    similarité textuelle vaut 0. Sans traitement particulier elle serait classée
    derrière n'importe quelle correspondance sur un nom, et donc écartée dès
    qu'il y a assez de résultats pour atteindre la limite."""
    # dix communes suffisent à elles seules à remplir les MAX_RESULTS places
    for i in range(1, 11):
        make_city(f"9000{i - 1}", f"Commune 20007034{i}", f"20007034{i}")

    response = api_client.get(URL, {"q": "200070340"})

    assert response.status_code == 200
    data = response.json()
    # l'EPCI prend la place d'une des dix communes, il n'est pas simplement ajouté
    assert data["epcis"] == [{"label": "CC des Deux Rives", "value": "200070340"}]
    assert len(data["cities"]) == 9
