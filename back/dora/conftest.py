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
