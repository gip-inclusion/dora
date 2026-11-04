from unittest.mock import patch

import pytest
from rest_framework.test import APIClient


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(config, items):
    """Active automatiquement la gestion de la db"""
    for item in items:
        markers = {marker.name for marker in item.iter_markers()}
        if "no_django_db" not in markers and "django_db" not in markers:
            item.add_marker(pytest.mark.django_db)


STRUCTURE_SOURCES = [
    ("porteur", "Porteur"),
    ("equipe-dora", "Équipe DORA"),
    ("invitations-masse", "Invitations en masse"),
    ("solidagregateur", "Solidagrégateur"),
]


@pytest.fixture(autouse=True)
def clear_geo_caches():
    """Vide les caches des managers de découpage administratif entre deux tests.

    Ces caches vivent pour toute la durée du process (les tables sont statiques
    en production) : sans cette remise à zéro, les divisions créées par un test
    resteraient visibles dans le suivant.
    """
    from dora.decoupage_administratif.models import EPCI, City, Department, Region

    managers = [City.objects, Department.objects, EPCI.objects, Region.objects]
    for manager in managers:
        manager._cache.clear()
    yield
    for manager in managers:
        manager._cache.clear()


@pytest.fixture(autouse=True)
def structure_sources(db):
    """Ensure structure sources exist for tests that create or join structures."""
    from dora.structures.models import StructureSource

    for value, label in STRUCTURE_SOURCES:
        StructureSource.objects.get_or_create(
            value=value,
            defaults={"label": label},
        )


@pytest.fixture(autouse=True, scope="session")
def patch_di_client():
    # Remplace le client D·I par défaut :
    # permet de s'affranchir de `settings.IS_TESTING` pour la plupart des cas.
    # Chaque test peut par la suite choisir son instance de client (fake).
    with patch("dora.data_inclusion.di_client_factory") as mocked_di_client:
        mocked_di_client.return_value = None
        yield


@pytest.fixture
def api_client():
    return APIClient()
