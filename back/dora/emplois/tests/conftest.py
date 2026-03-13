import pytest
from data_inclusion.schema.v0 import TypologieStructure
from model_bakery import baker

from dora.core.test_utils import make_published_service
from dora.services.models import FranceTravailOrientableService


@pytest.fixture(autouse=True)
def _set_emplois_email(settings):
    settings.EMPLOIS_EMAIL = "emplois@example.com"


@pytest.fixture
def emplois_user(api_client, settings):
    user = baker.make("users.User", is_valid=True, email=settings.EMPLOIS_EMAIL)
    api_client.force_authenticate(user=user)
    return user


@pytest.fixture
def published_service():
    return make_published_service()


@pytest.fixture
def orientable_service_via_dora_form(published_service):
    service = published_service
    service.contact_email = "contact@example.org"
    service.structure.disable_orientation_form = False
    service.structure.save()
    service.save()
    return service


@pytest.fixture
def ft_orientable_service(published_service):
    service = published_service
    service.structure.typology = TypologieStructure.FT
    service.structure.save()

    FranceTravailOrientableService.objects.create(
        structure=service.structure,
        service=service,
    )

    return service
