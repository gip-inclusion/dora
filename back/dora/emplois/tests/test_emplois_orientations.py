import uuid

import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_service
from dora.orientations.models import Orientation, OrientationStatus

ORIENTATION_URL = "emplois:orientation-list"
DEFAULT_DI_SERVICE_ID = "soliguide--svc-1"


def post_orientation(api_client, payload):
    return api_client.post(
        reverse(ORIENTATION_URL),
        data=payload,
        format="json",
    )


@pytest.fixture
def les_emplois_structure_id():
    return uuid.uuid4()


@pytest.fixture
def les_emplois_beneficiary_id():
    return uuid.uuid4()


@pytest.fixture
def base_payload(les_emplois_structure_id, les_emplois_beneficiary_id):
    return {
        "les_emplois_structure_id": str(les_emplois_structure_id),
        "les_emplois_beneficiary_id": str(les_emplois_beneficiary_id),
        "beneficiary_first_name": "Boris",
        "beneficiary_last_name": "Baracus",
        "referent_first_name": "Hannibal",
        "referent_last_name": "Smith",
        "referent_email": "hannibal@example.org",
    }


@pytest.fixture
def valid_payload(base_payload):
    return {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID}


def test_orientations_create_requires_authentication(api_client, base_payload):
    response = post_orientation(api_client, {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID})
    assert response.status_code == 401


def test_orientations_create_requires_emplois_email(api_client, valid_payload):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)
    response = post_orientation(api_client, valid_payload)
    assert response.status_code == 403


def test_orientations_create_with_dora_service_resolves_fk(
    emplois_user, api_client, base_payload
):
    service = make_service()

    response = post_orientation(
        api_client, {**base_payload, "di_service_id": f"dora--{service.id}"}
    )

    assert response.status_code == 201, response.data
    orientation = Orientation.objects.get()
    assert orientation.service_id == service.id
    assert orientation.di_service_id == ""
    # Représentation : on reconstitue di_service_id en sortie.
    assert response.data["di_service_id"] == f"dora--{service.id}"
    assert response.data["service"]["is_di"] is False
    assert response.data["service"]["slug"] == service.slug


def test_orientations_create_with_non_dora_service_keeps_di_id(
    emplois_user, api_client, base_payload
):
    response = post_orientation(
        api_client, {**base_payload, "di_service_id": "soliguide--svc-42"}
    )

    assert response.status_code == 201, response.data
    orientation = Orientation.objects.get()
    assert orientation.service is None
    assert orientation.di_service_id == "soliguide--svc-42"
    assert response.data["di_service_id"] == "soliguide--svc-42"
    assert response.data["service"]["is_di"] is True
    assert response.data["service"]["slug"] == "di--soliguide--svc-42"


@pytest.mark.parametrize("di_service_id", ["no-separator", ""])
def test_orientations_create_rejects_invalid_di_service_id(
    emplois_user, api_client, base_payload, di_service_id
):
    response = post_orientation(
        api_client, {**base_payload, "di_service_id": di_service_id}
    )
    assert response.status_code == 400
    assert "di_service_id" in response.data


@pytest.mark.parametrize("di_service_id", [f"dora--{uuid.uuid4()}", "dora--not-a-uuid"])
def test_orientations_create_with_unresolvable_dora_service(
    emplois_user, api_client, base_payload, di_service_id
):
    response = post_orientation(api_client, {**base_payload, "di_service_id": di_service_id})
    assert response.status_code == 404
    assert response.data["detail"]["code"] == "not_found"
    assert str(response.data["detail"]["message"]) == (
        "Service Dora introuvable pour cet identifiant."
    )


@pytest.mark.parametrize(
    "missing_field",
    [
        "beneficiary_first_name",
        "beneficiary_last_name",
        "referent_first_name",
        "referent_last_name",
        "referent_email",
        "di_service_id",
    ],
)
def test_orientations_create_requires_mandatory_fields(
    emplois_user, api_client, base_payload, missing_field
):
    payload = {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID}
    payload.pop(missing_field)

    response = post_orientation(api_client, payload)
    assert response.status_code == 400
    assert missing_field in response.data


def test_orientations_create_with_all_fields(emplois_user, api_client, base_payload):
    response = post_orientation(
        api_client,
        {
            **base_payload,
            "di_service_id": DEFAULT_DI_SERVICE_ID,
            "beneficiary_email": "boris@example.org",
            "beneficiary_phone": "0102030405",
            "beneficiary_other_contact_method": "Discord: boris#1234",
            "beneficiary_contact_preferences": ["EMAIL", "TELEPHONE"],
            "beneficiary_availability": "2026-05-15",
            "beneficiary_france_travail_number": "12345678901",
            "situation": ["RSA"],
            "situation_other": "En logement précaire",
            "requirements": ["Permis B"],
            "referent_phone": "0506070809",
        },
    )

    assert response.status_code == 201, response.data
    orientation = Orientation.objects.get()
    assert orientation.beneficiary_email == "boris@example.org"
    assert orientation.beneficiary_phone == "0102030405"
    assert orientation.beneficiary_contact_preferences == ["EMAIL", "TELEPHONE"]
    assert orientation.situation == ["RSA"]
    assert orientation.requirements == ["Permis B"]
    assert orientation.prescriber is None
    assert orientation.prescriber_structure is None
    assert orientation.status == OrientationStatus.PENDING
    assert orientation.les_emplois_structure_id == uuid.UUID(
        base_payload["les_emplois_structure_id"]
    )
