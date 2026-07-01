from .dora import (
    backend as _dora_backend,
)
from .dora import (
    send_orientation_created_to_structure as send_orientation_created_to_structure,
)
from .emplois import backend as _emplois_backend


def _backend(orientation):
    return (
        _emplois_backend
        if hasattr(orientation, "emplois_orientation_data")
        else _dora_backend
    )


def send_orientation_created_emails(orientation, cc=None):
    _backend(orientation).send_created(orientation)


def send_orientation_accepted_emails(
    orientation, prescriber_message, beneficiary_message
):
    _backend(orientation).send_accepted(
        orientation, prescriber_message, beneficiary_message
    )


def send_orientation_rejected_emails(orientation, message):
    _backend(orientation).send_rejected(orientation, message)


def send_orientation_expiration_emails(orientation, start_date):
    _backend(orientation).send_expired(orientation, start_date)


def send_orientation_reminder_emails(orientation):
    _backend(orientation).send_reminder(orientation)


def send_message_to_prescriber(orientation, message, cc):
    _backend(orientation).send_message_to_prescriber(orientation, message, cc)


def send_message_to_beneficiary(orientation, message, cc):
    _backend(orientation).send_message_to_beneficiary(orientation, message, cc)
