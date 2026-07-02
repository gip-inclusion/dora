import pytest
from django.core import mail
from django.utils import timezone

from dora.orientations.emails import (
    send_orientation_accepted_emails,
    send_orientation_created_emails,
    send_orientation_expiration_emails,
    send_orientation_rejected_emails,
    send_orientation_reminder_emails,
)

pytestmark = pytest.mark.django_db


EMAIL_SENDERS = [
    pytest.param(
        lambda o: send_orientation_created_emails(o), True, "created", id="created"
    ),
    pytest.param(
        lambda o: send_orientation_accepted_emails(
            o, "message presc.", "message bénéf."
        ),
        True,
        "accepted",
        id="accepted",
    ),
    pytest.param(
        lambda o: send_orientation_rejected_emails(o, message="Refus"),
        True,
        "rejected",
        id="rejected",
    ),
    pytest.param(
        lambda o: send_orientation_reminder_emails(o), True, "reminder", id="reminder"
    ),
    pytest.param(
        lambda o: send_orientation_expiration_emails(o, start_date=timezone.now()),
        False,
        "expired",
        id="expired",
    ),
]


@pytest.mark.parametrize("send_email, displays_structure_link, event", EMAIL_SENDERS)
def test_structure_email_displays_prescriber_info(
    orientation, send_email, displays_structure_link, event
):
    prescriber = orientation.prescriber_info

    send_email(orientation)

    structure_email = mail.outbox[0]
    assert structure_email.to == [orientation.get_contact_email()]
    assert prescriber.full_name in structure_email.body
    assert prescriber.structure_name in structure_email.body
    if displays_structure_link and prescriber.structure_url:
        assert prescriber.structure_url in structure_email.body


@pytest.mark.parametrize("send_email, displays_structure_link, event", EMAIL_SENDERS)
def test_prescriber_email_sent_to_correct_address(
    orientation, send_email, displays_structure_link, event
):
    send_email(orientation)

    recipients = [address for email in mail.outbox for address in email.to]

    # Les mails de relance des orientations créées
    # depuis les emplois ne sont envoyées qu'à l'offreur de service
    if event == "reminder" and orientation.comes_from_les_emplois():
        assert orientation.get_contact_email() in recipients
    else:
        assert orientation.prescriber_info.email in recipients
