import pytest
from django.core import mail

from dora.core.test_utils import make_service, make_structure, make_user
from dora.structures.models import ModerationStatus

from ..models import OrientationStatus


def test_query_refresh(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/refresh/"
    response = api_client.patch(url, follow=True)

    assert response.status_code == 204


def test_query_access(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/"
    response = api_client.get(url, follow=True)

    # permissions : pas de hash, pas d'orientation (pseudo-auth)
    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    response = api_client.get(url, follow=True)

    assert response.status_code == 200


def test_query_validate(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/validate/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "beneficiary_message": "test_beneficiary_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204
    assert orientation.status == OrientationStatus.ACCEPTED

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 4
    assert mail.outbox[0].to == [orientation.get_contact_email()]
    assert mail.outbox[1].to == [orientation.prescriber.email]
    assert mail.outbox[2].to == [orientation.referent_email]
    assert mail.outbox[3].to == [orientation.beneficiary_email]


def test_query_reject(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/reject/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "reasons": [],
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204
    assert orientation.status == OrientationStatus.REJECTED

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 3
    assert mail.outbox[0].to == [orientation.get_contact_email()]
    assert mail.outbox[1].to == [orientation.prescriber.email]
    assert mail.outbox[2].to == [orientation.referent_email]


def test_contact_beneficiary(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/contact/beneficiary/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [orientation.beneficiary_email]


def test_contact_prescriber(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/contact/prescriber/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [orientation.prescriber.email]


@pytest.mark.parametrize(
    "orientation_status",
    (OrientationStatus.MODERATION_PENDING, OrientationStatus.MODERATION_REJECTED),
)
@pytest.mark.parametrize(
    "path,method,data",
    [
        ("/refresh/", "patch", {}),
        ("/", "get", {}),
        (
            "/validate/",
            "post",
            {
                "message": "test_message",
                "beneficiary_message": "test_beneficiary_message",
            },
        ),
        (
            "/reject/",
            "post",
            {
                "message": "test_message",
                "reasons": [],
            },
        ),
        (
            "/contact/beneficiary/",
            "post",
            {
                "message": "test_message",
            },
        ),
        (
            "/contact/prescriber/",
            "post",
            {
                "message": "test_message",
            },
        ),
    ],
)
def test_moderation_error(
    api_client, orientation, orientation_status, path, method, data
):
    orientation.status = orientation_status
    orientation.save()

    url = f"/orientations/{orientation.query_id}{path}"

    if path != "/refresh/":
        url += f"?h={orientation.get_query_id_hash()}"

    response = getattr(api_client, method)(url, data=data, follow=True)

    assert response.status_code == 401


def get_new_dora_service_orientation_data(user, structure, service):
    return {
        "attachments": {},
        "beneficiaryAttachments": [],
        "beneficiaryAvailability": "2024-12-17",
        "beneficiaryContactPreferences": ["EMAIL"],
        "beneficiaryEmail": "beneficiary@example.com",
        "beneficiaryFirstName": "Beneficiary First Name",
        "beneficiaryLastName": "Beneficiary Last Name",
        "beneficiaryOtherContactMethod": "",
        "beneficiaryPhone": "",
        "contactBoxOpen": False,
        "diContactEmail": "",
        "diContactName": "",
        "diContactPhone": "",
        "diServiceId": "",
        "diServiceName": "",
        "diServiceAddressLine": "",
        "diStructureName": "",
        "firstStepDone": True,
        "orientationReasons": "",
        "prescriberStructureSlug": structure.slug,
        "referentEmail": "referent@example.com",
        "referentFirstName": "Referent First Name",
        "referentLastName": "Referent Last Name",
        "referentPhone": "0123456789",
        "requirements": [],
        "serviceSlug": service.slug,
        "situation": [],
    }


def get_new_di_service_orientation_data(user, structure, service):
    return {
        "attachments": {},
        "beneficiaryAttachments": [],
        "beneficiaryAvailability": "2024-12-17",
        "beneficiaryContactPreferences": ["EMAIL"],
        "beneficiaryEmail": "beneficiary@example.com",
        "beneficiaryFirstName": "Beneficiary First Name",
        "beneficiaryLastName": "Beneficiary Last Name",
        "beneficiaryOtherContactMethod": "",
        "beneficiaryPhone": "",
        "contactBoxOpen": False,
        "diContactEmail": "di.contact@example.com",
        "diContactName": "DI Contact",
        "diContactPhone": "0987654321",
        "diServiceId": "di--soliguide--630fa36e5c4d35d05bd267ab",
        "diServiceName": "DI Service Name",
        "diServiceAddressLine": "DI Address Line",
        "diStructureName": "DI Structure Name",
        "firstStepDone": True,
        "orientationReasons": "",
        "prescriberStructureSlug": structure.slug,
        "referentEmail": "referent@example.com",
        "referentFirstName": "Referent First Name",
        "referentLastName": "Referent Last Name",
        "referentPhone": "0123456789",
        "requirements": [],
        "serviceSlug": None,
        "situation": [],
    }


@pytest.mark.parametrize(
    "get_new_orientation_data",
    (get_new_dora_service_orientation_data, get_new_di_service_orientation_data),
)
@pytest.mark.parametrize(
    "moderation_status",
    (
        ModerationStatus.NEED_INITIAL_MODERATION,
        ModerationStatus.NEED_NEW_MODERATION,
        ModerationStatus.IN_PROGRESS,
    ),
)
def test_query_create_triggers_moderation(
    api_client, get_new_orientation_data, moderation_status
):
    user = make_user()
    structure = make_structure(user, moderation_status=moderation_status)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_orientation_data(user, structure, service)

    response = api_client.post("/orientations/", data=data, follow=True)

    assert response.status_code == 201
    assert response.data["status"] == "MODÉRATION_EN_COURS"

    assert structure.orientations.count() == 1

    orientation = structure.orientations.first()

    assert orientation.status == OrientationStatus.MODERATION_PENDING

    assert len(mail.outbox) == 0


@pytest.mark.parametrize(
    "get_new_orientation_data",
    (get_new_dora_service_orientation_data, get_new_di_service_orientation_data),
)
def test_query_create_does_not_trigger_moderation(api_client, get_new_orientation_data):
    user = make_user()
    structure = make_structure(user, moderation_status=ModerationStatus.VALIDATED)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_orientation_data(user, structure, service)

    response = api_client.post("/orientations/", data=data, follow=True)

    assert response.status_code == 201
    assert response.data["status"] == "OUVERTE"

    assert structure.orientations.count() == 1

    orientation = structure.orientations.first()

    assert orientation.status == OrientationStatus.PENDING

    assert len(mail.outbox) == 4
    assert mail.outbox[0].to == [orientation.get_contact_email()]
    assert mail.outbox[1].to == [orientation.prescriber.email]
    assert mail.outbox[2].to == [orientation.referent_email]
    assert mail.outbox[3].to == [orientation.beneficiary_email]
