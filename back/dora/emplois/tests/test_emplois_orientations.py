import json
import uuid
from datetime import timedelta
from unittest.mock import patch

import pytest
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.utils import timezone
from model_bakery import baker
from rest_framework.exceptions import ValidationError
from rest_framework.fields import DateTimeField

from dora.core.test_utils import make_orientation, make_service
from dora.orientations.models import (
    EmploisOrientationData,
    Orientation,
    OrientationStatus,
)

ORIENTATION_URL = "emplois:orientation-list"
ORIENTATION_STATUS_URL = "emplois:orientation-status"
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


def post_orientation(api_client, payload, attachments=None):
    data = {"data": json.dumps(payload)}
    if attachments:
        data["attachments"] = list(attachments)
    return api_client.post(
        reverse(ORIENTATION_URL),
        data=data,
        format="multipart",
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
    payload = {
        **base_payload,
        "di_service_id": f"dora--{service.id}",
    }

    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 201, response.data
    emplois_sync_uid = response.data.pop("emplois_sync_uid")

    assert response.data == payload
    orientation = Orientation.objects.get(service_id=service.id)
    assert orientation.emplois_orientation_data.emplois_sync_uid == emplois_sync_uid

    assert hasattr(orientation, "emplois_orientation_data")
    assert orientation.service_id == service.id
    assert orientation.di_service_id == ""


def test_orientations_create_with_non_dora_service_keeps_di_id(
    emplois_api_client, base_payload
):
    payload = {**base_payload, "di_service_id": "soliguide--svc-42"}
    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 201, response.data
    emplois_sync_uid = response.data.pop("emplois_sync_uid")

    assert response.data == payload
    orientation = Orientation.objects.get(di_service_id="soliguide--svc-42")
    assert orientation.emplois_orientation_data.emplois_sync_uid == emplois_sync_uid

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


@patch("dora.emplois.views.send_orientation_created_emails")
def test_orientations_create_with_all_fields(
    mock_send_created, emplois_api_client, base_payload
):
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
    # france_travail_number only returned once orientation is VALIDÉE
    emplois_sync_uid = response.data.pop("emplois_sync_uid")

    assert response.data == payload
    orientation = Orientation.objects.get(beneficiary_email="boris@example.org")
    assert orientation.emplois_orientation_data.emplois_sync_uid == emplois_sync_uid
    assert orientation.beneficiary_email == "boris@example.org"
    assert orientation.beneficiary_phone == "0102030405"
    assert orientation.beneficiary_contact_preferences == ["EMAIL", "TELEPHONE"]
    assert orientation.situation == ["RSA"]
    assert orientation.requirements == ["Permis B"]
    assert orientation.orientation_reasons == "Besoin d'accompagnement vers l'emploi"
    assert orientation.prescriber is None
    assert orientation.prescriber_structure is None
    assert orientation.status == OrientationStatus.PENDING

    mock_send_created.assert_called_once_with(orientation)

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


def test_orientations_create_without_attachments_stores_empty_list(
    emplois_api_client, valid_payload
):
    response = post_orientation(emplois_api_client, valid_payload)

    assert response.status_code == 201, response.data
    orientation = Orientation.objects.get(di_service_id=DEFAULT_DI_SERVICE_ID)
    assert orientation.beneficiary_attachments == []


def test_orientations_create_rejects_client_supplied_attachment_paths(
    emplois_api_client, valid_payload
):
    payload = {**valid_payload, "beneficiary_attachments": ["malicious/path.pdf"]}
    response = post_orientation(emplois_api_client, payload)

    assert response.status_code == 400
    assert "beneficiary_attachments" in response.data
    assert Orientation.objects.count() == 0


@patch("dora.emplois.views.save_orientation_attachment")
def test_orientations_create_with_attachments_uploads_in_one_call(
    mock_save_orientation_attachment,
    emplois_api_client,
    valid_payload,
):
    mock_save_orientation_attachment.side_effect = [
        "orientations/justificatif.pdf",
        "orientations/cv.pdf",
    ]
    attachments = [
        SimpleUploadedFile("justificatif.pdf", b"%PDF-1.4 fake"),
        SimpleUploadedFile("cv.pdf", b"%PDF-1.4 fake"),
    ]

    response = post_orientation(
        emplois_api_client, valid_payload, attachments=attachments
    )

    assert response.status_code == 201, response.data
    assert mock_save_orientation_attachment.call_count == 2

    expected_paths = ["orientations/justificatif.pdf", "orientations/cv.pdf"]
    orientation = Orientation.objects.get(di_service_id=DEFAULT_DI_SERVICE_ID)
    assert orientation.beneficiary_attachments == expected_paths
    assert response.data["beneficiary_attachments"] == expected_paths


@patch(
    "dora.emplois.views.save_orientation_attachment",
    return_value="orientations/justificatif.pdf",
)
@patch("dora.emplois.views.default_storage.delete")
def test_orientations_create_validates_before_uploading(
    mock_delete,
    mock_save_orientation_attachment,
    emplois_api_client,
    base_payload,
):
    # di_service_id manquant -> la validation du serializer échoue AVANT tout
    # upload : aucun fichier n'est envoyé ni supprimé sur S3.
    attachments = [SimpleUploadedFile("justificatif.pdf", b"%PDF-1.4 fake")]

    response = post_orientation(
        emplois_api_client, base_payload, attachments=attachments
    )

    assert response.status_code == 400
    assert mock_save_orientation_attachment.call_count == 0
    assert mock_delete.call_count == 0
    assert Orientation.objects.count() == 0


@patch("dora.emplois.views.save_orientation_attachment")
@patch("dora.emplois.views.default_storage.delete")
def test_orientations_create_cleans_up_uploads_when_an_upload_fails(
    mock_delete,
    mock_save_orientation_attachment,
    emplois_api_client,
    valid_payload,
):
    # if 2nd upload fails, the first file is deleted
    mock_save_orientation_attachment.side_effect = [
        "orientations/cv.pdf",
        ValidationError("FILE_TOO_BIG"),
    ]
    attachments = [
        SimpleUploadedFile("cv.pdf", b"%PDF-1.4 fake"),
        SimpleUploadedFile("too-big.pdf", b"%PDF-1.4 fake"),
    ]

    response = post_orientation(
        emplois_api_client, valid_payload, attachments=attachments
    )

    assert response.status_code == 400
    assert mock_save_orientation_attachment.call_count == 2
    mock_delete.assert_called_once_with("orientations/cv.pdf")
    assert Orientation.objects.count() == 0


def test_orientations_create_rejects_missing_data_part(emplois_api_client):
    response = emplois_api_client.post(
        reverse(ORIENTATION_URL),
        data={
            # no JSON
            "attachments": [SimpleUploadedFile("justificatif.pdf", b"%PDF-1.4 fake")]
        },
        format="multipart",
    )

    assert response.status_code == 400
    assert "data" in response.data


@patch("dora.emplois.views.send_orientation_created_emails")
def test_orientations_create_rolls_back_when_mail_sending_fails(
    mock_send_created, emplois_api_client, valid_payload
):
    mock_send_created.side_effect = RuntimeError("smtp down")

    with pytest.raises(RuntimeError):
        post_orientation(emplois_api_client, valid_payload)

    mock_send_created.assert_called_once()
    assert Orientation.objects.count() == 0


@patch("dora.emplois.views.default_storage.delete")
@patch(
    "dora.emplois.views.save_orientation_attachment",
    return_value="orientations/cv.pdf",
)
@patch("dora.emplois.views.send_orientation_created_emails")
def test_orientations_create_cleans_up_attachments_when_mail_sending_fails(
    mock_send_created,
    mock_save_orientation_attachment,
    mock_delete,
    emplois_api_client,
    valid_payload,
):
    mock_send_created.side_effect = RuntimeError("smtp down")
    attachments = [SimpleUploadedFile("cv.pdf", b"%PDF-1.4 fake")]

    with pytest.raises(RuntimeError):
        post_orientation(emplois_api_client, valid_payload, attachments=attachments)

    mock_save_orientation_attachment.assert_called_once()
    mock_delete.assert_called_once_with("orientations/cv.pdf")
    assert Orientation.objects.count() == 0


def test_orientations_create_rejects_invalid_data_json(emplois_api_client):
    response = emplois_api_client.post(
        reverse(ORIENTATION_URL),
        data={"data": "{not valid json"},
        format="multipart",
    )

    assert response.status_code == 400
    assert "data" in response.data


def make_emplois_orientation(**kwargs):
    """Crée une orientation émise par Les Emplois (avec ses `EmploisOrientationData`)."""
    orientation = baker.make(
        Orientation,
        di_service_id=DEFAULT_DI_SERVICE_ID,
        service=None,
        **kwargs,
    )
    baker.make(EmploisOrientationData, orientation=orientation)
    return orientation


def test_orientation_status_list_requires_authentication(api_client):
    response = api_client.get(reverse(ORIENTATION_STATUS_URL))
    assert response.status_code == 401


def test_orientation_status_list_requires_emplois_email(api_client):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)
    response = api_client.get(reverse(ORIENTATION_STATUS_URL))
    assert response.status_code == 403


def test_orientation_status_list_returns_only_emplois_orientations(
    emplois_api_client,
):
    processing_date = timezone.now()
    emplois_orientation = make_emplois_orientation(
        status=OrientationStatus.ACCEPTED,
        processing_date=processing_date,
    )
    # orientation Dora classique, sans données Les Emplois : exclue de la liste
    make_orientation()
    # orientation avec données Les Emplois mais avec un prescripteur Dora
    # (créée depuis un JWT Emplois) : exclue de la liste
    make_emplois_orientation(
        prescriber=baker.make("users.User", is_valid=True),
    )

    response = emplois_api_client.get(reverse(ORIENTATION_STATUS_URL))

    assert response.status_code == 200
    results = response.data["results"]
    assert len(results) == 1

    item = results[0]
    assert set(item.keys()) == {"emplois_sync_uid", "status", "updated_at"}
    assert item["emplois_sync_uid"] == str(
        emplois_orientation.emplois_orientation_data.emplois_sync_uid
    )
    assert item["status"] == OrientationStatus.ACCEPTED
    assert item["updated_at"] == DateTimeField().to_representation(processing_date)


def test_orientation_status_list_updated_at_falls_back_to_creation_date(
    emplois_api_client,
):
    # orientation pas encore traitée : pas de date de traitement
    orientation = make_emplois_orientation(status=OrientationStatus.PENDING)

    response = emplois_api_client.get(reverse(ORIENTATION_STATUS_URL))

    assert response.status_code == 200
    item = response.data["results"][0]
    assert item["updated_at"] == DateTimeField().to_representation(
        orientation.creation_date
    )


def test_orientation_status_list_filters_by_updated_after(emplois_api_client):
    cutoff = timezone.now()
    make_emplois_orientation(
        status=OrientationStatus.ACCEPTED,
        processing_date=cutoff - timedelta(days=1),
    )
    on_cutoff = make_emplois_orientation(
        status=OrientationStatus.REJECTED,
        processing_date=cutoff,
    )
    after_cutoff = make_emplois_orientation(
        status=OrientationStatus.ACCEPTED,
        processing_date=cutoff + timedelta(days=1),
    )

    response = emplois_api_client.get(
        reverse(ORIENTATION_STATUS_URL), {"updated_after": cutoff.isoformat()}
    )

    assert response.status_code == 200
    # borne incluse : l'orientation mise à jour exactement à `updated_after`
    # est retournée
    assert [item["emplois_sync_uid"] for item in response.data["results"]] == [
        str(on_cutoff.emplois_orientation_data.emplois_sync_uid),
        str(after_cutoff.emplois_orientation_data.emplois_sync_uid),
    ]


def test_orientation_status_list_rejects_invalid_updated_after(emplois_api_client):
    response = emplois_api_client.get(
        reverse(ORIENTATION_STATUS_URL), {"updated_after": "pas-une-date"}
    )

    assert response.status_code == 400
    assert "updated_after" in response.data


def test_orientation_status_list_ignores_empty_updated_after(emplois_api_client):
    make_emplois_orientation(status=OrientationStatus.PENDING)

    response = emplois_api_client.get(
        reverse(ORIENTATION_STATUS_URL), {"updated_after": ""}
    )

    # paramètre facultatif : vide, il est ignoré et la liste est complète
    assert response.status_code == 200
    assert len(response.data["results"]) == 1
