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
    orientation, send_email, displays_structure_link
):
    prescriber = orientation.prescriber_info

    send_email(orientation)

    structure_email = mail.outbox[0]
    assert structure_email.to == [orientation.get_contact_email()]
    assert prescriber.full_name in structure_email.body
    assert prescriber.structure_name in structure_email.body
    if displays_structure_link and prescriber.structure_url:
        assert prescriber.structure_url in structure_email.body


@pytest.mark.parametrize("send_email, displays_structure_link", EMAIL_SENDERS)
def test_prescriber_email_sent_to_correct_address(
    orientation, send_email, displays_structure_link
):
    send_email(orientation)

    recipients = [address for email in mail.outbox for address in email.to]
    assert orientation.prescriber_info.email in recipients
