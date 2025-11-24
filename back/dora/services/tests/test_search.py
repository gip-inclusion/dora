from unittest import mock

import pytest
from model_bakery import baker

from dora.admin_express.models import AdminDivisionType
from dora.core.test_utils import (
    make_published_service,
    make_service,
    make_structure,
    make_user,
)
from dora.data_inclusion.test_utils import FakeDataInclusionClient, make_di_service_data
from dora.services.enums import ServiceStatus


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


def test_search_services_with_obsolete_structure(api_client):
    # les services rattachés à une structure obsolète
    # doivent être filtrés lors de la recherche

    # Service publié avec structure non obsolète
    service = make_published_service(diffusion_zone_type=AdminDivisionType.COUNTRY)

    # le paramètre `city` est nécessaire a minima
    city = baker.make("City")

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
    api_client, orphan_service, structure_with_user
):
    # les services rattachés à une structure orpheline
    # doivent être filtrés lors de la recherche

    # le paramètre `city` est nécessaire a minima
    city = baker.make("City")

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


def test_search_services_includes_thematiques_empty_list(api_client):
    # Un service service DI ayant le champ thematiques avec une liste vide doit être retourné

    # le paramètre `city` est nécessaire a minima
    city = baker.make("City")

    with mock.patch("dora.data_inclusion.di_client_factory") as mock_di_client_factory:
        di_client = FakeDataInclusionClient()
        service = make_di_service_data(thematiques=[])
        di_client.services.append(service)

        mock_di_client_factory.return_value = di_client

        response = api_client.get(f"/search/?city={city.code}")

        assert response.status_code == 200

        assert len(response.data["services"]) == 1, "un service devrait être retourné"


def test_search_services_includes_thematiques_null(api_client):
    # Un service service DI ayant le champ thematiques à null doit être retourné

    # le paramètre `city` est nécessaire a minima
    city = baker.make("City")

    with mock.patch("dora.data_inclusion.di_client_factory") as mock_di_client_factory:
        di_client = FakeDataInclusionClient()
        service = make_di_service_data(thematiques=None)
        di_client.services.append(service)

        mock_di_client_factory.return_value = di_client

        response = api_client.get(f"/search/?city={city.code}")

        assert response.status_code == 200

        assert len(response.data["services"]) == 1, "un service devrait être retourné"
