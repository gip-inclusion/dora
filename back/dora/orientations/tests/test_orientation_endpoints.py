import pytest
from dateutil.relativedelta import relativedelta
from django.core import mail
from django.utils import timezone
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import (
    make_orientation,
    make_service,
    make_structure,
    make_user,
)
from dora.structures.models import ModerationStatus, StructureMember

from ..models import Orientation, OrientationStatus


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


def test_query_validate_service_di(api_client, di_orientation):
    url = f"/orientations/{di_orientation.query_id}/validate/?h={di_orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "beneficiary_message": "test_beneficiary_message",
    }
    response = api_client.post(url, data=data, follow=True)
    di_orientation.refresh_from_db()

    assert response.status_code == 204
    assert di_orientation.status == OrientationStatus.ACCEPTED

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 4
    assert mail.outbox[0].to == [di_orientation.get_contact_email()]
    assert mail.outbox[1].to == [di_orientation.prescriber.email]
    assert mail.outbox[2].to == [di_orientation.referent_email]
    assert mail.outbox[3].to == [di_orientation.beneficiary_email]


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
        "beneficiaryFranceTravailNumber": "12345678901",
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
        "dataProtectionCommitment": True,
    }


def get_new_di_service_orientation_data(user, structure, service):
    return {
        "attachments": {},
        "beneficiaryAttachments": [],
        "beneficiaryAvailability": "2024-12-17",
        "beneficiaryContactPreferences": ["EMAIL"],
        "beneficiaryEmail": "beneficiary@example.com",
        "beneficiaryFranceTravailNumber": "12345678901",
        "beneficiaryFirstName": "Beneficiary First Name",
        "beneficiaryLastName": "Beneficiary Last Name",
        "beneficiaryOtherContactMethod": "",
        "beneficiaryPhone": "",
        "contactBoxOpen": False,
        "diContactEmail": "di.contact@example.com",
        "diContactName": "DI Contact",
        "diContactPhone": "0987654321",
        "diServiceId": "soliguide--630fa36e5c4d35d05bd267ab",
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
        "dataProtectionCommitment": True,
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


def test_query_validate_service_duration_copy_on_orientation(api_client):
    service = make_service(duration_weekly_hours=6, duration_weeks=4)
    orientation = make_orientation(service=service)

    url = f"/orientations/{orientation.query_id}/validate/?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "beneficiary_message": "test_beneficiary_message",
    }
    api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert orientation.duration_weekly_hours == 6
    assert orientation.duration_weeks == 4


def test_create_with_data_protection_commitment(api_client):
    user = make_user()
    structure = make_structure(user, moderation_status=ModerationStatus.VALIDATED)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_dora_service_orientation_data(user, structure, service)

    data["dataProtectionCommitment"] = True

    response = api_client.post("/orientations/", data=data, follow=True)

    assert response.status_code == 201

    assert structure.orientations.count() == 1

    orientation = structure.orientations.first()

    assert orientation.data_protection_commitment


def test_create_without_data_protection_commitment(api_client):
    user = make_user()
    structure = make_structure(user, moderation_status=ModerationStatus.VALIDATED)
    service = make_service(contact_email="contact.service@example.com")

    api_client.force_authenticate(user=user)

    data = get_new_dora_service_orientation_data(user, structure, service)

    data["dataProtectionCommitment"] = False

    response = api_client.post("/orientations/", data=data, follow=True)

    assert response.status_code == 400
    assert "data_protection_commitment" in response.data

    assert structure.orientations.count() == 0


class OrientationStatsTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()
        self.service = make_service(structure=self.structure)
        self.user = make_user()
        baker.make(StructureMember, structure=self.structure, user=self.user)

        baker.make(
            Orientation,
            service=self.service,
            status=OrientationStatus.ACCEPTED,
        )
        baker.make(
            Orientation,
            service=self.service,
            status=OrientationStatus.PENDING,
        )

        baker.make(
            Orientation,
            service=self.service,
            prescriber_structure=self.structure,
            status=OrientationStatus.REJECTED,
        )
        baker.make(
            Orientation,
            service=self.service,
            prescriber_structure=self.structure,
            status=OrientationStatus.PENDING,
        )

        self.client.force_authenticate(user=self.user)

    def test_get_stats(self):
        with self.assertNumQueries(3):
            response = self.client.get(
                f"/structures/{self.structure.slug}/orientations/stats/"
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.data,
            {
                "total_sent": 2,
                "total_sent_pending": 1,
                "total_received": 4,
                "total_received_pending": 2,
                "structure_has_services": True,
            },
        )

    def test_raise_403_when_user_not_structure_member(self):
        self.client.force_authenticate(user=make_user())

        response = self.client.get(
            f"/structures/{self.structure.slug}/orientations/stats/"
        )

        self.assertEqual(response.status_code, 403)


class OrientationsExportTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()
        self.service = make_service(structure=self.structure)
        self.user = make_user()
        baker.make(StructureMember, structure=self.structure, user=self.user)

        self.client.force_authenticate(user=self.user)

    def test_get_export_of_sent_orientations(self):
        prescriber = make_user()

        orientation_1 = baker.make(
            Orientation,
            creation_date=timezone.now() - relativedelta(days=1),
            service=self.service,
            status=OrientationStatus.ACCEPTED,
            prescriber_structure=self.structure,
            prescriber=prescriber,
        )

        orientation_2 = baker.make(
            Orientation,
            creation_date=timezone.now() - relativedelta(days=2),
            service=self.service,
            status=OrientationStatus.MODERATION_PENDING,
            prescriber_structure=self.structure,
            prescriber=None,
        )

        # Assurer que cette orientation n'est pas incluse dans les résultats
        baker.make(
            Orientation,
            service=make_service(),
        )

        with self.assertNumQueries(3):
            response = self.client.get(
                f"/structures/{self.structure.slug}/orientations/export/?type=sent"
            )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data,
            [
                {
                    "creation_date": orientation_1.creation_date.strftime("%Y-%m-%d"),
                    "status": "Validée",
                    "beneficiary_name": orientation_1.get_beneficiary_full_name(),
                    "prescriber_name": prescriber.get_full_name(),
                    "structure_name": orientation_1.get_structure_name(),
                    "service_name": orientation_1.get_service_name(),
                },
                {
                    "creation_date": orientation_2.creation_date.strftime("%Y-%m-%d"),
                    "status": "En cours de modération",
                    "beneficiary_name": orientation_2.get_beneficiary_full_name(),
                    "prescriber_name": "Utilisateur supprimé",
                    "structure_name": orientation_2.get_structure_name(),
                    "service_name": orientation_2.get_service_name(),
                },
            ],
        )

    def test_get_export_of_received_orientations(self):
        prescriber = make_user()

        orientation_1 = baker.make(
            Orientation,
            creation_date=timezone.now() - relativedelta(days=1),
            service=self.service,
            status=OrientationStatus.ACCEPTED,
            prescriber_structure=self.structure,
            prescriber=prescriber,
        )

        orientation_2 = baker.make(
            Orientation,
            creation_date=timezone.now() - relativedelta(days=2),
            service=self.service,
            status=OrientationStatus.MODERATION_PENDING,
            prescriber_structure=None,
            prescriber=None,
        )

        # Assurer que cette orientation n'est pas incluse dans les résultats
        baker.make(
            Orientation,
            service=make_service(),
        )

        with self.assertNumQueries(3):
            response = self.client.get(
                f"/structures/{self.structure.slug}/orientations/export/?type=received"
            )

        self.assertEqual(response.status_code, 200)

        self.assertEqual(len(response.data), 2)
        self.assertEqual(
            response.data,
            [
                {
                    "creation_date": orientation_1.creation_date.strftime("%Y-%m-%d"),
                    "status": "Validée",
                    "beneficiary_name": orientation_1.get_beneficiary_full_name(),
                    "prescriber_name": prescriber.get_full_name(),
                    "prescriber_structure_name": orientation_1.prescriber_structure.name,
                    "service_name": orientation_1.get_service_name(),
                    "detail_page_url": orientation_1.get_magic_link(),
                },
                {
                    "creation_date": orientation_2.creation_date.strftime("%Y-%m-%d"),
                    "status": "En cours de modération",
                    "beneficiary_name": orientation_2.get_beneficiary_full_name(),
                    "prescriber_name": "Utilisateur supprimé",
                    "prescriber_structure_name": "Pas de prescripteur",
                    "service_name": orientation_2.get_service_name(),
                    "detail_page_url": orientation_2.get_magic_link(),
                },
            ],
        )

    def test_raise_403_if_user_not_structure_member(self):
        self.client.force_authenticate(user=make_user())

        response = self.client.get(
            f"/structures/{self.structure.slug}/orientations/export/?type=sent"
        )

        self.assertEqual(response.status_code, 403)

    def test_raise_400_when_invalid_orientation_type(self):
        response = self.client.get(
            f"/structures/{self.structure.slug}/orientations/export/?type=other"
        )

        self.assertEqual(response.status_code, 400)
