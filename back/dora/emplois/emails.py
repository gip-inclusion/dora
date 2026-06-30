from django.conf import settings
from django.template.loader import render_to_string
from mjml import mjml2html

from dora.core.emails import send_mail

debug = settings.ORIENTATION_EMAILS_DEBUG


def _has_distinct_referent(orientation):
    return (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    )


def _get_service_name(orientation):
    if orientation.service_id:
        return orientation.service.name
    return orientation.di_service_name


def _get_service_address(orientation):
    if orientation.service is None:
        return orientation.di_service_address_line
    elif (
        orientation.service.location_kinds.count() == 1
        and orientation.service.location_kinds.first().value == "a-distance"
    ):
        return "à distance"
    else:
        return orientation.get_service_address_line()


def send_orientation_created(orientation):
    context = {
        "data": orientation,
        "service_address": _get_service_address(orientation),
        "service_name": _get_service_name(orientation),
    }

    send_mail(
        f"{'[Envoyée - Emplois Prescripteur] ' if debug else ''}Votre demande a bien été transmise !",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-creation-prescriber.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Envoyée - Emplois Conseiller référent] ' if debug else ''}Notification d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(render_to_string("orientation-creation-referent.mjml", context)),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Envoyée - Emplois Bénéficiaire] ' if debug else ''}Une orientation a été effectuée en votre nom",
        orientation.beneficiary_email,
        mjml2html(render_to_string("orientation-creation-beneficiary.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.prescriber_info.email],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_orientation_accepted(orientation, prescriber_message, beneficiary_message):
    context = {
        "data": orientation,
        "prescriber_message": prescriber_message,
        "beneficiary_message": beneficiary_message,
        "service_name": _get_service_name(orientation),
    }

    send_mail(
        f"{'[Validée - Emplois Prescripteur] ' if debug else ''}Votre demande a été acceptée ! 🎉",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-accepted-prescriber.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Validée - Emplois Conseiller référent] ' if debug else ''}Notification de l’acceptation d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(render_to_string("orientation-accepted-referent.mjml", context)),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Validée - Emplois Bénéficiaire] ' if debug else ''}Votre demande a été acceptée ! 🎉",
        orientation.beneficiary_email,
        mjml2html(render_to_string("orientation-accepted-beneficiary.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_orientation_rejected(orientation, message, other_details=""):
    context = {
        "data": orientation,
        "message": message,
        "other_details": other_details,
        "service_name": _get_service_name(orientation),
    }

    send_mail(
        f"{'[Refusée - Emplois Bénéficiaire] ' if debug else ''}Votre demande d’orientation a été refusée",
        orientation.beneficiary_email,
        mjml2html(render_to_string("orientation-rejected-beneficiary.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    send_mail(
        f"{'[Refusée - Emplois Prescripteur] ' if debug else ''}Votre demande d’orientation a été refusée",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-rejected-prescriber.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Refusée - Emplois Conseiller référent] ' if debug else ''}Votre demande d’orientation a été refusée",
            orientation.referent_email,
            mjml2html(
                render_to_string("orientation-rejected-prescriber.mjml", context)
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )


def send_orientation_expired(orientation, start_date=None):
    context = {
        "data": orientation,
        "service_name": _get_service_name(orientation),
    }

    send_mail(
        f"{'[Expirée - Emplois Prescripteur] ' if debug else ''}Votre demande d’orientation a expiré",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-expired-prescriber.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )

    if _has_distinct_referent(orientation):
        send_mail(
            f"{'[Expirée - Emplois Conseiller référent] ' if debug else ''}Votre demande d’orientation a expiré",
            orientation.referent_email,
            mjml2html(render_to_string("orientation-expired-prescriber.mjml", context)),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
            from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
        )

    send_mail(
        f"{'[Expirée - Emplois Bénéficiaire] ' if debug else ''}Cette demande d’orientation a été annulée",
        orientation.beneficiary_email,
        mjml2html(render_to_string("orientation-expired-beneficiary.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )


def send_orientation_contact_message_from_offerer(orientation, message):
    context = {
        "data": orientation,
        "message": message,
        "service_name": _get_service_name(orientation),
    }

    send_mail(
        f"{'[Contact - Emplois Bénéficiaire] ' if debug else ''}Vous avez un nouveau message",
        orientation.beneficiary_email,
        mjml2html(
            render_to_string("orientation-offreur-contact-message.mjml", context)
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        from_email=("La plateforme de l'inclusion", settings.NO_REPLY_EMAIL),
    )
