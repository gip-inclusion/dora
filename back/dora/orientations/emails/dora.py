from types import SimpleNamespace

from django.conf import settings
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django.utils import timezone
from mjml import mjml2html

from dora.core.emails import send_mail
from dora.orientations.models import ContactPreference, Orientation

debug = settings.ORIENTATION_EMAILS_DEBUG


def beneficiaries_has_alternate_contact_methods(orientation):
    beneficiaries_contact_methods = [
        method
        for method in [
            orientation.beneficiary_phone,
            orientation.beneficiary_email,
            orientation.beneficiary_other_contact_method,
        ]
        if method
    ]

    return len(beneficiaries_contact_methods) > len(
        orientation.beneficiary_contact_preferences
    )


def _orientation_created_ctx(orientation) -> dict:
    return {
        "data": orientation,
        "ContactPreference": ContactPreference,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        "beneficiaries_has_alternate_contact_methods": beneficiaries_has_alternate_contact_methods(
            orientation
        ),
        "service_address": orientation.get_service_address_line(),
        "attachments": [
            {"name": a, "url": default_storage.url(a)}
            for a in orientation.beneficiary_attachments
        ],
    }


def send_orientation_created_to_structure(orientation, context=None):
    if not context:
        context = _orientation_created_ctx(orientation)

    send_mail(
        f"{'[Envoyée - Structure porteuse] ' if debug else ''}Nouvelle demande d’orientation reçue",
        orientation.get_contact_email(),
        mjml2html(render_to_string("orientation-created-structure.mjml", context)),
        from_email=(
            f"{orientation.prescriber_info.full_name} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        ),
        tags=["orientation"],
        reply_to=[orientation.prescriber_info.email],
    )


def send_orientation_created_to_prescriber(orientation, context=None):
    if not context:
        context = _orientation_created_ctx(orientation)

    send_mail(
        f"{'[Envoyée - Prescripteur] ' if debug else ''}Votre demande a bien été transmise !",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-created-prescriber.mjml", context)),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
    )


def send_orientation_created_to_referent(orientation, context=None):
    if not context:
        context = _orientation_created_ctx(orientation)

    if (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    ):
        send_mail(
            f"{'[Envoyée - Conseiller référent] ' if debug else ''}Notification d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(render_to_string("orientation-created-referent.mjml", context)),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
        )


def send_orientation_created_to_beneficiary(orientation, context=None):
    if not context:
        context = _orientation_created_ctx(orientation)

    if orientation.beneficiary_email:
        send_mail(
            f"{'[Envoyée - Bénéficiaire] ' if debug else ''}Une orientation a été effectuée en votre nom",
            orientation.beneficiary_email,
            mjml2html(
                render_to_string("orientation-created-beneficiary.mjml", context)
            ),
            from_email=(
                f"{orientation.prescriber_info.full_name} via DORA",
                settings.DEFAULT_FROM_EMAIL,
            ),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
        )


def _dora_send_created(orientation):
    context = _orientation_created_ctx(orientation)

    send_orientation_created_to_structure(orientation, context)
    send_orientation_created_to_prescriber(orientation, context)
    send_orientation_created_to_referent(orientation, context)
    send_orientation_created_to_beneficiary(orientation, context)


def _orientation_accepted_ctx(
    orientation, prescriber_message="", beneficiary_message=""
):
    placeholder = "#SERVICE_ADDRESS#"
    prescriber_message = prescriber_message.replace(
        placeholder, orientation.get_service_address_line()
    )
    beneficiary_message = beneficiary_message.replace(
        placeholder, orientation.get_service_address_line()
    )

    return {
        "data": orientation,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        "prescriber_message": prescriber_message,
        "beneficiary_message": beneficiary_message,
    }


def send_orientation_accepted_to_structure(orientation, context=None):
    if not context:
        context = _orientation_accepted_ctx(orientation)

    send_mail(
        f"{'[Validée - Structure porteuse] ' if debug else ''}Vous venez de valider une demande 🎉",
        [orientation.get_contact_email()],
        mjml2html(render_to_string("orientation-accepted-structure.mjml", context)),
        tags=["orientation"],
    )


def send_orientation_accepted_to_prescriber(orientation, context=None):
    if not context:
        context = _orientation_accepted_ctx(orientation)

    send_mail(
        f"{'[Validée - Prescripteur] ' if debug else ''}Votre demande a été acceptée ! 🎉",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("orientation-accepted-prescriber.mjml", context)),
        from_email=(
            f"{orientation.get_structure_name()} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
    )


def send_orientation_accepted_to_referent(orientation, context=None):
    if not context:
        context = _orientation_accepted_ctx(orientation)

    if (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    ):
        send_mail(
            f"{'[Validée - Conseiller référent] ' if debug else ''}Notification de l’acceptation d’une demande d’orientation",
            orientation.referent_email,
            mjml2html(render_to_string("orientation-accepted-referent.mjml", context)),
            from_email=(
                f"{orientation.get_structure_name()} via DORA",
                settings.DEFAULT_FROM_EMAIL,
            ),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
        )


def send_orientation_accepted_to_beneficiary(orientation, context=None):
    if not context:
        context = _orientation_accepted_ctx(orientation)

    if orientation.beneficiary_email:
        send_mail(
            f"{'[Validée - Bénéficiaire] ' if debug else ''}Votre demande a été acceptée ! 🎉",
            orientation.beneficiary_email,
            mjml2html(
                render_to_string("orientation-accepted-beneficiary.mjml", context)
            ),
            from_email=(
                f"{orientation.get_structure_name()} via DORA",
                settings.DEFAULT_FROM_EMAIL,
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
        )


def _dora_send_accepted(orientation, prescriber_message, beneficiary_message):
    context = _orientation_accepted_ctx(
        orientation, prescriber_message, beneficiary_message
    )

    send_orientation_accepted_to_structure(orientation, context)
    send_orientation_accepted_to_prescriber(orientation, context)
    send_orientation_accepted_to_referent(orientation, context)
    send_orientation_accepted_to_beneficiary(orientation, context)


def _orientation_rejected_ctx(orientation, message=""):
    return {
        "data": orientation,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        "message": message,
    }


def send_orientation_rejected_to_structure(orientation, context=None):
    if not context:
        context = _orientation_rejected_ctx(orientation)

    send_mail(
        f"{'[Refusée - Structure porteuse] ' if debug else ''}Vous venez de refuser une demande",
        [orientation.get_contact_email()],
        mjml2html(render_to_string("orientation-rejected-structure.mjml", context)),
        tags=["orientation"],
    )


def send_orientation_rejected_to_beneficiary(orientation, context=None):
    if not context:
        context = _orientation_rejected_ctx(orientation)

    if orientation.beneficiary_email:
        send_mail(
            f"{'[Refusée - Bénéficiaire] ' if debug else ''}Votre demande d’orientation a été refusée",
            [orientation.beneficiary_email],
            mjml2html(
                render_to_string("orientation-rejected-beneficiary.mjml", context)
            ),
            from_email=(
                f"{orientation.get_structure_name()} via DORA",
                settings.DEFAULT_FROM_EMAIL,
            ),
            tags=["orientation"],
            reply_to=[orientation.prescriber_info.email],
        )


def send_orientation_rejected_to_prescriber(orientation, context=None):
    if not context:
        context = _orientation_rejected_ctx(orientation)

    send_mail(
        f"{'[Refusée - Prescripteur] ' if debug else ''}Votre demande d’orientation a été refusée",
        [orientation.prescriber_info.email],
        mjml2html(render_to_string("orientation-rejected-prescriber.mjml", context)),
        from_email=(
            f"{orientation.get_structure_name()} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
    )


def send_orientation_rejected_to_referent(orientation, context=None):
    if not context:
        context = _orientation_rejected_ctx(orientation)

    if (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    ):
        send_mail(
            f"{'[Refusée - Conseiller référent] ' if debug else ''}Votre demande d’orientation a été refusée",
            [orientation.referent_email],
            mjml2html(
                render_to_string("orientation-rejected-prescriber.mjml", context)
            ),
            from_email=(
                f"{orientation.get_structure_name()} via DORA",
                settings.DEFAULT_FROM_EMAIL,
            ),
            tags=["orientation"],
            reply_to=[orientation.get_contact_email()],
        )


def _dora_send_rejected(orientation, message):
    context = _orientation_rejected_ctx(orientation, message)

    send_orientation_rejected_to_structure(orientation, context)
    send_orientation_rejected_to_beneficiary(orientation, context)
    send_orientation_rejected_to_prescriber(orientation, context)
    send_orientation_rejected_to_referent(orientation, context)


def _dora_send_message_to_prescriber(orientation, message, cc):
    context = {
        "data": orientation,
        "message": message,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
    }
    send_mail(
        f"{'[Contact - Prescripteur] ' if debug else ''}Vous avez un nouveau message 📩",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("contact-prescriber.mjml", context)),
        from_email=(
            f"{orientation.get_structure_name()} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        cc=cc,
    )


def _dora_send_message_to_beneficiary(orientation, message, cc):
    context = {
        "data": orientation,
        "message": message,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
    }

    send_mail(
        f"{'[Contact - Bénéficiaire] ' if debug else ''}Vous avez un nouveau message 📩",
        orientation.beneficiary_email,
        mjml2html(render_to_string("contact-beneficiary.mjml", context)),
        from_email=(
            f"{orientation.get_structure_name()} via DORA",
            settings.DEFAULT_FROM_EMAIL,
        ),
        tags=["orientation"],
        reply_to=[orientation.get_contact_email()],
        cc=cc,
    )


def _orientation_reminder_ctx(orientation):
    return {
        "data": orientation,
        "support_email": settings.SUPPORT_EMAIL,
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        "elapsed_days": (timezone.now() - orientation.creation_date).days,
        "ContactPreference": ContactPreference,
        "beneficiaries_has_alternate_contact_methods": beneficiaries_has_alternate_contact_methods(
            orientation
        ),
        "attachments": [
            {"name": a, "url": default_storage.url(a)}
            for a in orientation.beneficiary_attachments
        ],
    }


def send_orientation_reminder_to_structure(orientation, context=None):
    if not context:
        context = _orientation_reminder_ctx(orientation)

    send_mail(
        f"{'[Notification - Structure] ' if debug else ''}Relance – Demande d’orientation en attente",
        orientation.get_contact_email(),
        mjml2html(render_to_string("notification-structure.mjml", context)),
        tags=["orientation"],
    )


def _dora_send_reminder(orientation):
    context = _orientation_reminder_ctx(orientation)

    send_orientation_reminder_to_structure(orientation, context)

    cc = []
    if (
        orientation.referent_email
        and orientation.referent_email != orientation.prescriber_info.email
    ):
        cc.append(orientation.referent_email)

    send_mail(
        f"{'[Notification - Prescripteur] ' if debug else ''}Relance envoyée – Demande d’orientation en attente",
        orientation.prescriber_info.email,
        mjml2html(render_to_string("notification-prescriber.mjml", context)),
        tags=["orientation"],
        cc=cc,
    )


def _orientation_expired_ctx(orientation, start_date):
    return {
        "data": orientation,
        "expiration_period_days": settings.ORIENTATION_EXPIRATION_PERIOD_DAYS,
        "search_link": settings.FRONTEND_URL + "/recherche",
        "start_date": start_date.strftime("%-d %B %Y"),
        "orientation_support_link": settings.ORIENTATION_SUPPORT_LINK,
        "with_dora_info": True,
        "with_legal_info": True,
    }


def send_orientation_expired_to_structure(orientation, context):
    send_mail(
        "Cette demande d’orientation a expiré",
        orientation.get_contact_email(),
        mjml2html(render_to_string("orientation-expired-service.mjml", context)),
        tags=["orientation"],
    )


def _dora_send_expired(orientation: Orientation, start_date) -> None:
    context = _orientation_expired_ctx(orientation, start_date)

    send_orientation_expired_to_structure(orientation, context)

    send_mail(
        "Cette demande d’orientation a été annulée",
        orientation.beneficiary_email,
        mjml2html(render_to_string("orientation-expired-beneficiary.mjml", context)),
        tags=["orientation"],
    )

    for email in {orientation.prescriber_info.email, orientation.referent_email}:
        send_mail(
            "Votre demande d’orientation a expiré",
            email,
            mjml2html(render_to_string("orientation-expired-prescriber.mjml", context)),
            tags=["orientation"],
        )


backend = SimpleNamespace(
    send_created=_dora_send_created,
    send_accepted=_dora_send_accepted,
    send_rejected=_dora_send_rejected,
    send_expired=_dora_send_expired,
    send_reminder=_dora_send_reminder,
    send_message_to_prescriber=_dora_send_message_to_prescriber,
    send_message_to_beneficiary=_dora_send_message_to_beneficiary,
)
