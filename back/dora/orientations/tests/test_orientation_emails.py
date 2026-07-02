from dataclasses import dataclass
from typing import Callable

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
from dora.orientations.models import Orientation


@dataclass
class EmailScenario:
    send: Callable[[Orientation], None]
    structure_email_links_to_prescriber_structure: bool
    notifies_prescriber: bool


SCENARIOS = [
    pytest.param(
        EmailScenario(
            send=send_orientation_created_emails,
            structure_email_links_to_prescriber_structure=True,
            notifies_prescriber=True,
        ),
        id="created",
    ),
    pytest.param(
        EmailScenario(
            send=lambda o: send_orientation_accepted_emails(
                o,
                prescriber_message="message presc.",
                beneficiary_message="message bénéf.",
            ),
            structure_email_links_to_prescriber_structure=True,
            notifies_prescriber=True,
        ),
        id="accepted",
    ),
    pytest.param(
        EmailScenario(
            send=lambda o: send_orientation_rejected_emails(o, message="Refus"),
            structure_email_links_to_prescriber_structure=True,
            notifies_prescriber=True,
        ),
        id="rejected",
    ),
    pytest.param(
        EmailScenario(
            send=send_orientation_reminder_emails,
            structure_email_links_to_prescriber_structure=True,
            notifies_prescriber=False,
        ),
        id="reminder",
    ),
    pytest.param(
        EmailScenario(
            send=lambda o: send_orientation_expiration_emails(
                o, start_date=timezone.now()
            ),
            structure_email_links_to_prescriber_structure=False,
            notifies_prescriber=True,
        ),
        id="expired",
    ),
]


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_structure_email_displays_prescriber_info(orientation, scenario):
    scenario.send(orientation)

    structure_email = mail.outbox[0]
    prescriber = orientation.prescriber_info

    assert structure_email.to == [orientation.get_contact_email()]
    assert prescriber.full_name in structure_email.body
    assert prescriber.structure_name in structure_email.body
    if (
        scenario.structure_email_links_to_prescriber_structure
        and prescriber.structure_url
    ):
        assert prescriber.structure_url in structure_email.body


@pytest.mark.parametrize("scenario", SCENARIOS)
def test_prescriber_is_notified_only_when_expected(orientation, scenario):
    scenario.send(orientation)

    recipients = {address for email in mail.outbox for address in email.to}

    if scenario.notifies_prescriber:
        assert orientation.prescriber_info.email in recipients
    else:
        assert orientation.prescriber_info.email not in recipients
