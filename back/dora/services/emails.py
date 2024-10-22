import datetime

from django.conf import settings
from django.template.loader import render_to_string
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail


def send_service_feedback_email(service, full_name, email, message):
    html_message = message.replace("\n", "<br>")
    body = f"""
        <html><body>
        Suggestion d’amélioration envoyée par {full_name} ({email}) pour le service:<br>
        “<a href="{settings.FRONTEND_URL}/services/{service.slug}">{service.name}</a>” de la structure<br>
        “<a href="{settings.FRONTEND_URL}/structures/{service.structure.slug}">{service.structure.name}</a> ({service.structure.department})”<br>

        Le contact du service est {service.contact_name} ({service.contact_email} {service.contact_phone})<br>
        Le contact de la structure est <a href="mailto:{service.structure.email}">{service.structure.email}</a><br>
        <hr><br><br>
        {html_message}
        </body>
        """

    send_mail(
        f"[{settings.ENVIRONMENT}] Suggestion d'amélioration de service",
        settings.SUPPORT_EMAIL,
        body,
        tags=["feedback"],
    )


def send_service_sharing_email(
    service, sender_name, recipient_email, recipient_kind, is_di
):
    cta_link = (
        furl(settings.FRONTEND_URL)
        / "services"
        / f"{'di--' if is_di else ''}{service['slug']}"
    )
    cta_link.add(
        {
            "mtm_campaign": "FicheService",
            "mtm_kwd": "PartagerLaFiche",
        }
    )

    service_email = ""
    if service["is_contact_info_public"]:
        service_email = (
            service["contact_email"] or service["structure_info"]["email"] or ""
        )
    else:
        service_email = service["structure_info"]["email"] or ""

    service_phone = ""
    if service["is_contact_info_public"]:
        service_phone = (
            service["contact_phone"] or service["structure_info"]["phone"] or ""
        )
    else:
        service_phone = service["structure_info"]["phone"] or ""

    modes = []
    if recipient_kind == "professional":
        for mode in zip(
            service["coach_orientation_modes"] or [],
            service["coach_orientation_modes_display"] or [],
        ):
            if mode[0] == "autre":
                modes.append(service["coach_orientation_modes_other"] or "")
            else:
                modes.append(mode[1])
    else:
        all_beneficiaries_modes = [
            mode for mode in service["beneficiaries_access_modes"] or []
        ]
        if "se-presenter" in all_beneficiaries_modes:
            modes.append("Se présenter")
        if "envoyer-un-mail" in all_beneficiaries_modes and service_email:
            modes.append(f"Envoyer un mail: {service_email}")
        if "telephoner" in all_beneficiaries_modes and service_phone:
            modes.append(f"Téléphoner: {service_phone}")
        if (
            "autre" in all_beneficiaries_modes
            and service["beneficiaries_access_modes_other"]
        ):
            modes.append(service["beneficiaries_access_modes_other"])

    context = {
        "sender_name": sender_name,
        "service": service,
        "cta_link": cta_link,
        "with_legal_info": True,
        "with_dora_info": True,
        "publics": [s for s in service["concerned_public_display"] or []]
        or ["Tous publics"],
        "requirements": [
            *[ac for ac in service["access_conditions_display"] or []],
            *[r for r in service["requirements_display"] or []],
        ]
        or ["Aucun"],
        "modes": modes,
        "for_beneficiary": recipient_kind == "beneficiary",
    }

    send_mail(
        "On vous a recommandé une solution solidaire",
        recipient_email,
        mjml2html(render_to_string("sharing-email.mjml", context)),
        tags=["service-sharing"],
    )


def send_service_reminder_email(
    recipient_email, recipient_name, structures_to_update, structures_with_drafts
):
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
