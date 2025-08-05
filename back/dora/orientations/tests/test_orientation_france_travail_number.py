from dora.core.test_utils import (
    make_service,
    make_structure,
    make_user,
)
from dora.orientations.models import OrientationStatus
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


def test_france_travail_number_visibility_by_status(api_client):
    """Test que le numéro France Travail n'est visible que quand l'orientation est validée."""
    user = make_user()
    structure = make_structure(user, moderation_status=ModerationStatus.VALIDATED)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_dora_service_orientation_data(user, structure, service)
    data["beneficiaryFranceTravailNumber"] = "12345678901"

    # Créer l'orientation
    response = api_client.post("/orientations/", data=data, follow=True)
    assert response.status_code == 201

    orientation = structure.orientations.first()
    assert orientation.beneficiary_france_travail_number == "12345678901"

    # Tester tous les statuts possibles
    test_cases = [
        # (statut, devrait_être_visible, devrait_être_accessible)
        (OrientationStatus.MODERATION_PENDING, False, False),
        (OrientationStatus.MODERATION_REJECTED, False, False),
        (OrientationStatus.PENDING, False, True),
        (OrientationStatus.ACCEPTED, True, True),
        (OrientationStatus.REJECTED, False, True),
    ]

    for status, should_be_visible, should_be_accessible in test_cases:
        orientation.status = status
        orientation.save()

        url = (
            f"/orientations/{orientation.query_id}/?h={orientation.get_query_id_hash()}"
        )
        response = api_client.get(url, follow=True)

        if should_be_accessible:
            assert response.status_code == 200
            if should_be_visible:
                assert (
                    response.data["beneficiary_france_travail_number"] == "12345678901"
                )
            else:
                assert response.data["beneficiary_france_travail_number"] == ""
        else:
            # Les orientations en modération ne sont pas accessibles
            assert response.status_code in [401, 403]
