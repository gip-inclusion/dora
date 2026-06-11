import pytest
from django.core import mail
from django.utils import timezone

from dora.core.test_utils import make_emplois_orientation, make_orientation
from dora.orientations.emails import (
    _orientation_prescriber_context,
    send_orientation_accepted_emails,
    send_orientation_created_emails,
    send_orientation_expiration_emails,
    send_orientation_rejected_emails,
    send_orientation_reminder_emails,
)

pytestmark = pytest.mark.django_db

EMPLOIS_FRONTEND_URL = "https://emplois.inclusion.beta.gouv.fr"


def test_prescriber_context_dora_orientation():
    orientation = make_orientation()

    context = _orientation_prescriber_context(orientation)

    assert context == {
        "prescriber_full_name": orientation.prescriber.get_full_name(),
        "prescriber_structure_name": orientation.prescriber_structure.name,
        "prescriber_structure_url": orientation.prescriber_structure.get_frontend_url(),
    }


def test_prescriber_context_emplois_orientation(settings):
    settings.EMPLOIS_FRONTEND_URL = EMPLOIS_FRONTEND_URL
    orientation = make_emplois_orientation()

    context = _orientation_prescriber_context(orientation)

    assert context == {
        "prescriber_full_name": "Jean-Prescripteur des Emplois",
        "prescriber_structure_name": "Structure des Emplois",
        "prescriber_structure_url": orientation.emplois_orientation_data.structure_url,
    }


def test_prescriber_context_dora_orientation_without_prescriber():
    orientation = make_orientation(prescriber=None)

    context = _orientation_prescriber_context(orientation)

    assert context == {
        "prescriber_full_name": "",
        "prescriber_structure_name": orientation.prescriber_structure.name,
        "prescriber_structure_url": orientation.prescriber_structure.get_frontend_url(),
    }


def test_prescriber_context_dora_orientation_without_structure():
    orientation = make_orientation(prescriber_structure=None)

    context = _orientation_prescriber_context(orientation)

    assert context == {
        "prescriber_full_name": orientation.prescriber.get_full_name(),
        "prescriber_structure_name": "",
        "prescriber_structure_url": "",
    }


@pytest.fixture(params=["dora", "emplois"])
def orientation_and_prescriber(request, settings):
    """Renvoie (orientation, infos prescripteur attendues) selon la source."""
    if request.param == "dora":
        orientation = make_orientation(beneficiary_email="beneficiary@example.com")
        prescriber = {
            "email": orientation.prescriber.email,
            "full_name": orientation.prescriber.get_full_name(),
            "structure_name": orientation.prescriber_structure.name,
            "structure_url": orientation.prescriber_structure.get_frontend_url(),
        }
    else:
        settings.EMPLOIS_FRONTEND_URL = EMPLOIS_FRONTEND_URL
        orientation = make_emplois_orientation(
            beneficiary_email="beneficiary@example.com"
        )
        prescriber = {
            "email": orientation.emplois_orientation_data.prescriber_email,
            "full_name": orientation.emplois_orientation_data.prescriber_full_name,
            "structure_name": orientation.emplois_orientation_data.structure_name,
            "structure_url": orientation.emplois_orientation_data.structure_url,
        }
    return orientation, prescriber


EMAIL_SENDERS = [
    pytest.param(lambda o: send_orientation_created_emails(o), True, id="created"),
    pytest.param(
        lambda o: send_orientation_accepted_emails(
            o, "message presc.", "message bénéf."
        ),
        True,
        id="accepted",
    ),
    pytest.param(
        lambda o: send_orientation_rejected_emails(o, message="Refus"),
        True,
        id="rejected",
    ),
    pytest.param(lambda o: send_orientation_reminder_emails(o), True, id="reminder"),
    pytest.param(
        lambda o: send_orientation_expiration_emails(o, start_date=timezone.now()),
        False,
        id="expired",
    ),
]


@pytest.mark.parametrize("send_email, displays_structure_link", EMAIL_SENDERS)
def test_structure_email_displays_prescriber_info(
    orientation_and_prescriber, send_email, displays_structure_link
):
    orientation, prescriber = orientation_and_prescriber

    send_email(orientation)

    structure_email = mail.outbox[0]
    assert structure_email.to == [orientation.get_contact_email()]
    assert prescriber["full_name"] in structure_email.body
    assert prescriber["structure_name"] in structure_email.body
    if displays_structure_link:
        assert prescriber["structure_url"] in structure_email.body


@pytest.mark.parametrize("send_email, displays_structure_link", EMAIL_SENDERS)
def test_prescriber_email_sent_to_correct_address(
    orientation_and_prescriber, send_email, displays_structure_link
):
    orientation, prescriber = orientation_and_prescriber

    send_email(orientation)

    recipients = [address for email in mail.outbox for address in email.to]
    assert prescriber["email"] in recipients
