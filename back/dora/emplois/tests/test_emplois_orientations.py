import uuid

import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_service
from dora.orientations.models import (
    Orientation,
    OrientationStatus,
)

ORIENTATION_URL = "emplois:orientation-list"
DEFAULT_DI_SERVICE_ID = "soliguide--svc-1"

EMPLOIS_DATA = {
    "beneficiary_id": str(uuid.uuid4()),
    "structure_id": str(uuid.uuid4()),
    "structure_name": "Mission locale Paris",
    "structure_siret": "12345678901234",
    "prescriber_id": str(uuid.uuid4()),
    "prescriber_email": "prescripteur@example.org",
    "prescriber_first_name": "Alice",
    "prescriber_last_name": "Martin",
    "prescriber_phone": "0142030405",
}


def post_orientation(api_client, payload):
    return api_client.post(
        reverse(ORIENTATION_URL),
        data=payload,
        format="json",
    )


@pytest.fixture
def base_payload():
    return {
        "emplois_data": dict(EMPLOIS_DATA),
        "beneficiary_first_name": "Boris",
        "beneficiary_last_name": "Baracus",
        "referent_first_name": "Hannibal",
        "referent_last_name": "Smith",
        "referent_email": "hannibal@example.org",
        "data_protection_commitment": True,
    }


@pytest.fixture
def valid_payload(base_payload):
    return {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID}


def test_orientations_create_requires_authentication(api_client, valid_payload):
    response = post_orientation(api_client, valid_payload)
    assert response.status_code == 401


def test_orientations_create_requires_emplois_email(api_client, valid_payload):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)
    response = post_orientation(api_client, valid_payload)
    assert response.status_code == 403


def test_orientations_create_with_dora_service_resolves_fk(
    emplois_api_client, base_payload
):
    service = make_service()
    payload = {**base_payload, "di_service_id": f"dora--{service.id}"}
    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 201, response.data
    assert response.data == payload
    orientation = Orientation.objects.get(service_id=service.id)
    assert hasattr(orientation, "emplois_orientation_data")
    assert orientation.service_id == service.id
    assert orientation.di_service_id == ""


def test_orientations_create_with_non_dora_service_keeps_di_id(
    emplois_api_client, base_payload
):
    payload = {**base_payload, "di_service_id": "soliguide--svc-42"}
    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 201, response.data
    assert response.data == payload
    orientation = Orientation.objects.get(di_service_id="soliguide--svc-42")
    assert hasattr(orientation, "emplois_orientation_data")
    assert orientation.service is None
    assert orientation.di_service_id == "soliguide--svc-42"


@pytest.mark.parametrize(
    "include_field,value",
    [(False, None), (True, False)],
    ids=["missing", "false"],
)
def test_orientations_create_requires_data_protection_commitment(
    emplois_api_client, base_payload, include_field, value
):
    payload = {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID}
    payload.pop("data_protection_commitment", None)
    if include_field:
        payload["data_protection_commitment"] = value

    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 400
    assert "data_protection_commitment" in response.data
    assert Orientation.objects.count() == 0


@pytest.mark.parametrize("di_service_id", ["no-separator", ""])
def test_orientations_create_rejects_invalid_di_service_id(
    emplois_api_client, base_payload, di_service_id
):
    response = post_orientation(
        emplois_api_client, {**base_payload, "di_service_id": di_service_id}
    )
    assert response.status_code == 400
    assert "di_service_id" in response.data


@pytest.mark.parametrize("di_service_id", [f"dora--{uuid.uuid4()}", "dora--not-a-uuid"])
def test_orientations_create_with_unresolvable_dora_service(
    emplois_api_client, base_payload, di_service_id
):
    response = post_orientation(
        emplois_api_client, {**base_payload, "di_service_id": di_service_id}
    )
    assert response.status_code == 404
    assert response.data["detail"]["code"] == "not_found"
    assert str(response.data["detail"]["message"]) == (
        "Service Dora introuvable pour cet identifiant."
    )


@pytest.mark.parametrize(
    "parent_field,missing_field",
    [
        (None, "beneficiary_first_name"),
        (None, "beneficiary_last_name"),
        (None, "referent_first_name"),
        (None, "referent_last_name"),
        (None, "referent_email"),
        (None, "di_service_id"),
        ("emplois_data", "beneficiary_id"),
        ("emplois_data", "structure_id"),
    ],
)
def test_orientations_create_requires_mandatory_fields(
    emplois_api_client, base_payload, parent_field, missing_field
):
    payload = {**base_payload, "di_service_id": DEFAULT_DI_SERVICE_ID}
    if parent_field is None:
        payload.pop(missing_field)
    else:
        payload[parent_field] = {
            k: v for k, v in payload[parent_field].items() if k != missing_field
        }

    response = post_orientation(emplois_api_client, payload)
    assert response.status_code == 400
    if parent_field is None:
        assert missing_field in response.data
    else:
        assert parent_field in response.data
        assert missing_field in response.data[parent_field]


@pytest.mark.parametrize(
    "missing_emplois_field",
    [
        "beneficiary_id",
        "structure_id",
        "structure_name",
        "structure_siret",
        "prescriber_id",
        "prescriber_email",
        "prescriber_first_name",
        "prescriber_last_name",
        "prescriber_phone",
    ],
)
def test_orientations_create_requires_all_emplois_data_fields(
    emplois_api_client, base_payload, missing_emplois_field
):
    payload = {
        **base_payload,
        "di_service_id": DEFAULT_DI_SERVICE_ID,
        "emplois_data": {
            k: v for k, v in EMPLOIS_DATA.items() if k != missing_emplois_field
        },
    }

    response = post_orientation(emplois_api_client, payload)
    assert response.status_code == 400
    assert "emplois_data" in response.data
    assert missing_emplois_field in response.data["emplois_data"]


def test_orientations_create_with_all_fields(emplois_api_client, base_payload):
    payload = {
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
        "orientation_reasons": "Besoin d'accompagnement vers l'emploi",
    }
    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 201, response.data
    assert response.data == payload
    orientation = Orientation.objects.get(beneficiary_email="boris@example.org")
    assert orientation.beneficiary_email == "boris@example.org"
    assert orientation.beneficiary_phone == "0102030405"
    assert orientation.beneficiary_contact_preferences == ["EMAIL", "TELEPHONE"]
    assert orientation.situation == ["RSA"]
    assert orientation.requirements == ["Permis B"]
    assert orientation.orientation_reasons == "Besoin d'accompagnement vers l'emploi"
    assert orientation.prescriber is None
    assert orientation.prescriber_structure is None
    assert orientation.status == OrientationStatus.PENDING

    data = orientation.emplois_orientation_data
    assert data.structure_name == EMPLOIS_DATA["structure_name"]
    assert data.structure_siret == EMPLOIS_DATA["structure_siret"]
    assert data.prescriber_id == uuid.UUID(EMPLOIS_DATA["prescriber_id"])
    assert data.prescriber_email == EMPLOIS_DATA["prescriber_email"]
    assert data.prescriber_first_name == EMPLOIS_DATA["prescriber_first_name"]
    assert data.prescriber_last_name == EMPLOIS_DATA["prescriber_last_name"]
    assert data.prescriber_phone == EMPLOIS_DATA["prescriber_phone"]
    assert data.structure_id == uuid.UUID(EMPLOIS_DATA["structure_id"])
    assert data.beneficiary_id == uuid.UUID(EMPLOIS_DATA["beneficiary_id"])


def test_orientations_create_rejects_invalid_structure_siret(
    emplois_api_client, base_payload
):
    response = post_orientation(
        emplois_api_client,
        {
            **base_payload,
            "di_service_id": DEFAULT_DI_SERVICE_ID,
            "emplois_data": {**EMPLOIS_DATA, "structure_siret": "abc"},
        },
    )

    assert response.status_code == 400
    assert "emplois_data" in response.data
    assert "structure_siret" in response.data["emplois_data"]
