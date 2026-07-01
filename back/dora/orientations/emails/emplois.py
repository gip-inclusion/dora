from types import SimpleNamespace

from django.conf import settings
from django.template.loader import render_to_string
from mjml import mjml2html

from dora.core.emails import send_mail

from .dora import (
    _orientation_accepted_ctx,
    _orientation_expired_ctx,
    _orientation_rejected_ctx,
    send_orientation_accepted_to_structure,
    send_orientation_created_to_structure,
    send_orientation_expired_to_structure,
    send_orientation_rejected_to_structure,
    send_orientation_reminder_to_structure,
)

debug = settings.ORIENTATION_EMAILS_DEBUG


def _has_distinct_referent(orientation):
    return (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    )


def _get_service_address(orientation):
    if (
        orientation.service
        and orientation.service.location_kinds.count() == 1
        and orientation.service.location_kinds.first().value == "a-distance"
    ):
        return "à distance"
    return orientation.get_service_address_line()


def send_orientation_created(orientation):
    context = {
        "data": orientation,
        "service_address": _get_service_address(orientation),
    }

    send_mail(
        f"{'[Envoyée - Emplois Prescripteur] ' if debug else ''}Votre demande a bien été transmise !",
        orientation.prescriber_info.email,
        mjml2html(
            render_to_string("emplois/orientation-creation-prescriber.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Envoyée - Emplois Conseiller référent] ' if debug else ''}Notification d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(
                render_to_string("emplois/orientation-creation-referent.mjml", context)
            ),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Envoyée - Emplois Bénéficiaire] ' if debug else ''}Une orientation a été effectuée en votre nom",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("emplois/orientation-creation-beneficiary.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.prescriber_info.email],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_orientation_accepted(orientation, prescriber_message, beneficiary_message):
    placeholder = "#SERVICE_ADDRESS#"
    service_address = _get_service_address(orientation)
    prescriber_message = prescriber_message.replace(placeholder, service_address)
    beneficiary_message = beneficiary_message.replace(placeholder, service_address)

    context = {
        "data": orientation,
        "prescriber_message": prescriber_message,
        "beneficiary_message": beneficiary_message,
    }

    send_mail(
        f"{'[Validée - Emplois Prescripteur] ' if debug else ''}Votre demande a été acceptée ! 🎉",
        orientation.prescriber_info.email,
        mjml2html(
            render_to_string("emplois/orientation-accepted-prescriber.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Validée - Emplois Conseiller référent] ' if debug else ''}Notification de l’acceptation d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(
                render_to_string("emplois/orientation-accepted-referent.mjml", context)
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Validée - Emplois Bénéficiaire] ' if debug else ''}Votre demande a été acceptée ! 🎉",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("emplois/orientation-accepted-beneficiary.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_orientation_rejected(orientation, message, other_details=""):
    context = {
        "data": orientation,
        "message": message,
        "other_details": other_details,
    }

    send_mail(
        f"{'[Refusée - Emplois Bénéficiaire] ' if debug else ''}Votre demande d’orientation a été refusée",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("emplois/orientation-rejected-beneficiary.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    send_mail(
        f"{'[Refusée - Emplois Prescripteur] ' if debug else ''}Votre demande d’orientation a été refusée",
        orientation.prescriber_info.email,
        mjml2html(
            render_to_string("emplois/orientation-rejected-prescriber.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Refusée - Emplois Conseiller référent] ' if debug else ''}Votre demande d’orientation a été refusée",
            orientation.referent_email,
            mjml2html(
                render_to_string(
                    "emplois/orientation-rejected-prescriber.mjml", context
                )
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )


def send_orientation_expired(orientation, start_date=None):
    context = {
        "data": orientation,
    }

    send_mail(
        f"{'[Expirée - Emplois Prescripteur] ' if debug else ''}Votre demande d’orientation a expiré",
        orientation.prescriber_info.email,
        mjml2html(
            render_to_string("emplois/orientation-expired-prescriber.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Expirée - Emplois Conseiller référent] ' if debug else ''}Votre demande d’orientation a expiré",
            orientation.referent_email,
            mjml2html(
                render_to_string("emplois/orientation-expired-prescriber.mjml", context)
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Expirée - Emplois Bénéficiaire] ' if debug else ''}Cette demande d’orientation a été annulée",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("emplois/orientation-expired-beneficiary.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_message_to_prescriber(orientation, message, cc):
    context = {
        "data": orientation,
        "message": message,
    }

    structure_name = orientation.prescriber_info.structure_name

    send_mail(
        f"{'[Contact - Emplois Prescripteur] ' if debug else ''}Vous avez un nouveau message de la structure {structure_name}",
        orientation.prescriber_info.email,
        mjml2html(
            render_to_string("emplois/orientation-contact-prescriber.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=(
            f"{structure_name} via Les Emplois",
            settings.DEFAULT_FROM_EMAIL,
        ),
        cc=cc,
    )


def send_message_to_beneficiary(orientation, message, cc):
    structure_name = orientation.prescriber_info.structure_name
    context = {
        "data": orientation,
        "message": message,
        "structure_name": structure_name,
    }

    send_mail(
        f"{'[Contact - Emplois Bénéficiaire] ' if debug else ''}Vous avez un nouveau message de la structure {structure_name}",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("emplois/orientation-contact-beneficiary.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=(
            f"{structure_name} via Les Emplois",
            settings.DEFAULT_FROM_EMAIL,
        ),
        cc=cc,
    )


def _emplois_send_created(orientation):
    send_orientation_created_to_structure(orientation)
    send_orientation_created(orientation)


def _emplois_send_accepted(orientation, prescriber_message, beneficiary_message):
    send_orientation_accepted_to_structure(
        orientation,
        _orientation_accepted_ctx(orientation, prescriber_message, beneficiary_message),
    )
    send_orientation_accepted(orientation, prescriber_message, beneficiary_message)


def _emplois_send_rejected(orientation, message):
    send_orientation_rejected_to_structure(
        orientation, _orientation_rejected_ctx(orientation, message)
    )
    send_orientation_rejected(orientation, message)


def _emplois_send_expired(orientation, start_date):
    send_orientation_expired_to_structure(
        orientation, _orientation_expired_ctx(orientation, start_date)
    )
    send_orientation_expired(orientation, start_date)


def _emplois_send_reminder(orientation):
    send_orientation_reminder_to_structure(orientation)


backend = SimpleNamespace(
    send_created=_emplois_send_created,
    send_accepted=_emplois_send_accepted,
    send_rejected=_emplois_send_rejected,
    send_expired=_emplois_send_expired,
    send_reminder=_emplois_send_reminder,
    send_message_to_prescriber=send_message_to_prescriber,
    send_message_to_beneficiary=send_message_to_beneficiary,
)
