from django.conf import settings
from django.template.loader import render_to_string
from django.utils.encoding import iri_to_uri

from dora.core.emails import send_mail


def send_suggestion_validated_new_structure_email(email, structure):
    params = {
        "structure": structure,
        "cta_link": f"{settings.FRONTEND_URL}/auth/rattachement?siret={structure.siret}&login_hint={iri_to_uri(email)}",
    }
    body = render_to_string("new_structure.html", params)

    send_mail(
        "[DORA] Des acteurs de l’insertion sont intéressés par vos services !",
        email,
        body,
        tags=["validate_suggestion_new_structure"],
    )


def send_suggestion_validated_existing_structure_email(
    to, structure, service, contact_email
):
    params = {
        "structure": structure,
        "cta_link": service.get_frontend_url(),
        "contact_email": contact_email if contact_email not in to else None,
    }
    body = render_to_string("existing_structure.html", params)

    send_mail(
        "[DORA] Vous avez reçu une nouvelle suggestion de service ! 🥳 🎉",
        to,
        body,
        tags=["validate_suggestion_existing_structure"],
    )
