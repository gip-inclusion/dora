from unittest.mock import patch

import pytest
from rest_framework.test import APIClient


@pytest.fixture(autouse=True, scope="session")
def patch_di_client():
    # Remplace le client D·I par défaut :
    # permet de s'affranchir de `settings.IS_TESTING` pour la plupart des cas.
    # Chaque test peut par la suite choisir son instance de client (fake).
    with patch("dora.data_inclusion.di_client_factory") as mocked_di_client:
        mocked_di_client.return_value = None
        yield


@pytest.fixture(autouse=True)
def _use_db(db):
    # Active automatiquement la gestion de la db
    # (ce qui n'est pas fait par défaut avec pytest).
    pass


@pytest.fixture
def api_client():
    return APIClient()
