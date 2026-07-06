from .dora import (
    send_orientation_created_to_structure as send_orientation_created_to_structure,
)


def send_orientation_created_emails(orientation, cc=None):
    orientation.email_backend().send_created(orientation)


def send_orientation_accepted_emails(
    orientation, prescriber_message, beneficiary_message
):
    orientation.email_backend().send_accepted(
        orientation, prescriber_message, beneficiary_message
    )


def send_orientation_rejected_emails(orientation, message):
    orientation.email_backend().send_rejected(orientation, message)


def send_orientation_expiration_emails(orientation, start_date):
    orientation.email_backend().send_expired(orientation, start_date)


def send_orientation_reminder_emails(orientation):
    orientation.email_backend().send_reminder(orientation)


def send_message_to_prescriber(orientation, message, cc):
    orientation.email_backend().send_message_to_prescriber(orientation, message, cc)


def send_message_to_beneficiary(orientation, message, cc):
    orientation.email_backend().send_message_to_beneficiary(orientation, message, cc)
