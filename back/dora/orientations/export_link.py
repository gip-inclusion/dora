from django.conf import settings
from django.core import signing
from django.template.loader import render_to_string
from furl import furl
from mjml import mjml2html

from dora.core.emails import send_mail

# Durée de validité du lien de téléchargement, en secondes
EXPORT_LINK_MAX_AGE = 10 * 60

EXPORT_TYPES = ("sent", "received")

_SALT = "orientations-export"


def make_export_token(user, structure, export_type: str) -> str:
    return signing.dumps(
        {
            "user_id": str(user.pk),
            "structure_slug": structure.slug,
            "type": export_type,
        },
        salt=_SALT,
    )


def read_export_token(token: str) -> dict:
    """Lève ``signing.SignatureExpired`` si le jeton est périmé,
    ``signing.BadSignature`` s'il est invalide.
    """
    return signing.loads(token, salt=_SALT, max_age=EXPORT_LINK_MAX_AGE)


def build_export_url(user, structure, export_type: str) -> str:
    url = furl(settings.FRONTEND_URL) / "orientations" / "telechargement"
    url.add(
        {
            "structure": structure.slug,
            "type": export_type,
            "token": make_export_token(user, structure, export_type),
        }
    )
    return url.url


def send_export_link(user, structure, export_type: str) -> None:
    context = {
        "type_label": "envoyées" if export_type == "sent" else "reçues",
        "download_link": build_export_url(user, structure, export_type),
    }
    send_mail(
        "Votre lien de téléchargement du fichier des orientations DORA",
        user.email,
        mjml2html(render_to_string("orientations-export-link.mjml", context)),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["orientation"],
    )
