from dora.core.test_utils import (
    make_service,
    make_structure,
    make_user,
)
from dora.orientations.tests.test_orientation_endpoints import (
    get_new_dora_service_orientation_data,
)
from dora.structures.models import ModerationStatus


def test_create_with_france_travail_number(api_client):
    user = make_user()
    structure = make_structure(user, moderation_status=ModerationStatus.VALIDATED)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_dora_service_orientation_data(user, structure, service)

    response = api_client.post("/orientations/", data=data, follow=True)

    assert response.status_code == 201

    assert structure.orientations.count() == 1

    orientation = structure.orientations.first()

    assert (
        orientation.beneficiary_france_travail_number
        == data["beneficiaryFranceTravailNumber"]
    )
