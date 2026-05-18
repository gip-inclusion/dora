import datetime

from django.conf import settings
from django.template.loader import render_to_string
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail
from dora.services.models import Service


def send_service_feedback_email(
    service_name,
    service_url,
    is_di,
    recipients,
    notify_support,
    reasons,
    name,
    email,
    details,
):
    bcc = (
        [settings.SUPPORT_EMAIL] if notify_support and settings.SUPPORT_EMAIL else None
    )

    if not recipients and not bcc:
        return

    context = {
        "service_name": service_name,
        "service_url": service_url,
        "is_di": is_di,
        "reasons": reasons,
        "name": name,
        "email": email,
        "details": details,
    }

    send_mail(
        f"[{settings.ENVIRONMENT}] Signalement de modification pour votre service référencé sur DORA",
        recipients,
        mjml2html(render_to_string("service-feedback-email.mjml", context)),
        tags=["feedback"],
        bcc=bcc,
        reply_to=[f"{name} <{email}>"],
    )


def send_service_reminder_email(
    recipient_email,
    recipient_name,
    structures_to_update,
    structures_with_drafts,
):
    # déprécié : utiliser le système de notification et `send_service_notification`
    today = datetime.date.today()
    for structure in structures_to_update:
        utms = f"utm_source=NotifTransacDora&utm_medium=email&utm_campaign=Actualisation-{today.year}-{today.month:02}"
        redirect = f"/structures/{structure.slug}/services?update-status=ALL&{utms}"
        structure.link = furl(settings.FRONTEND_URL).add(
            path="/auth/connexion",
            args={
                "next": redirect,
            },
        )
    for structure in structures_with_drafts:
        utms = f"utm_source=NotifTransacDora&utm_medium=email&utm_campaign=Brouillon-{today.year}-{today.month:02}"
        redirect = f"/structures/{structure.slug}/services?service-status=DRAFT&{utms}"
        structure.link = furl(settings.FRONTEND_URL).add(
            path="/auth/connexion",
            args={
                "next": redirect,
            },
        )

    params = {
        "recipient_email": recipient_email,
        "recipient_name": recipient_name,
        "structures_to_update": structures_to_update,
        "structures_with_drafts": structures_with_drafts,
    }
    body = render_to_string("email_services_check.html", params)
    send_mail(
        "Des mises à jour de votre offre de service sur DORA sont nécessaires",
        recipient_email,
        body,
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["services_check"],
    )


def send_service_notification(service_editor):
    # à terme doit remplacer `send_service_reminder_email` dont la management command sera supprimé
    services = Service.objects.expired_drafts() | Service.objects.update_advised()
    draft_services = services.filter(contact_email=service_editor.email)[:5]
    services_to_update = services.filter(history_item__user=service_editor)[:5]
    draft_structure = draft_services[0].structure if draft_services else None
    update_structure = services_to_update[0].structure if services_to_update else None
    cta_draft_services_link = (
        furl(settings.FRONTEND_URL).add(
            path="/auth/connexion",
            args={
                "next": f"/structures/{draft_structure.slug}/services?service-status=DRAFT",
            },
        )
        if draft_structure
        else ""
    )
    cta_services_to_update_link = (
        furl(settings.FRONTEND_URL).add(
            path="/auth/connexion",
            args={
                "next": f"/structures/{update_structure.slug}/services?update-status=ALL",
            },
        )
        if update_structure
        else ""
    )

    context = {
        "user": service_editor,
        "draft_services": draft_services,
        "services_to_update": services_to_update,
        # CTA brouillons et actualisation
        "cta_draft_services_link": cta_draft_services_link,
        "cta_services_to_update_link": cta_services_to_update_link,
        # liens d'aide
        "help_update_services_url": "https://aide.dora.inclusion.gouv.fr/fr/article/actualiser-ses-services-1u0a101/",
    }

    send_mail(
        "Des mises à jour de votre offre de service sur DORA sont nécessaires",
        service_editor.email,
        mjml2html(render_to_string("notification-services.mjml", context)),
        tags=["service-notification"],
    )
