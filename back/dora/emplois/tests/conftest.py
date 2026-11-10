import pytest
from model_bakery import baker


@pytest.fixture(autouse=True)
def _set_emplois_email(settings):
    settings.EMPLOIS_EMAIL = "emplois@example.com"


@pytest.fixture
def emplois_api_client(api_client, settings):
    user = baker.make("users.User", is_valid=True, email=settings.EMPLOIS_EMAIL)
    api_client.force_authenticate(user=user)
    return api_client
