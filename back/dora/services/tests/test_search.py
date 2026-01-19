from unittest import mock

import pytest
from model_bakery import baker
from rest_framework import serializers

from dora.admin_express.models import AdminDivisionType
from dora.core.test_utils import (
    make_published_service,
    make_service,
    make_structure,
    make_user,
)
from dora.data_inclusion.test_utils import FakeDataInclusionClient, make_di_service_data
from dora.services.enums import ServiceStatus
from dora.services.views import _validate_search_categories_and_subcategories


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
    city = baker.make("admin_express.City")

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
    city = baker.make("admin_express.City")

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
    city = baker.make("admin_express.City")

    with mock.patch("dora.data_inclusion.di_client_factory") as mock_di_client_factory:
        di_client = FakeDataInclusionClient()
        service = make_di_service_data(zone_eligibilite=[city.code], thematiques=[])
        di_client.services.append(service)

        mock_di_client_factory.return_value = di_client

        response = api_client.get(f"/search/?city={city.code}")

        assert response.status_code == 200

        assert len(response.data["services"]) == 1, "un service devrait être retourné"


def test_search_services_includes_thematiques_null(api_client):
    # Un service service DI ayant le champ thematiques à null doit être retourné

    # le paramètre `city` est nécessaire a minima
    city = baker.make("admin_express.City")

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

        with pytest.raises(serializers.ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=["invalid_cat"], subcategories_list=None
            )

        assert "Catégories invalides" in str(exc_info.value)

    def test_validate_invalid_subcategories(self):
        """Teste que les sous-catégories invalides sont rejetées."""
        baker.make("ServiceSubCategory", value="cat1--sub1", label="Sous-catégorie 1")

        with pytest.raises(serializers.ValidationError) as exc_info:
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

        with pytest.raises(serializers.ValidationError) as exc_info:
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

        with pytest.raises(serializers.ValidationError) as exc_info:
            _validate_search_categories_and_subcategories(
                categories_list=None, subcategories_list=["cat1--obsolete_sub"]
            )

        assert "Sous-catégories invalides" in str(exc_info.value)


def test_search_endpoint_rejects_invalid_categories(api_client):
    """Teste que le endpoint de recherche rejette les catégories invalides."""
    city = baker.make("admin_express.City")
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


def test_search_endpoint_rejects_invalid_subcategories(api_client):
    """Teste que le endpoint de recherche rejette les sous-catégories invalides."""
    city = baker.make("admin_express.City")
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
