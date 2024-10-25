from django.conf import settings
from django.template.loader import render_to_string
from mjml import mjml2html

from dora.core.emails import send_mail


def send_authentication_link(email, magic_link):
    context = {"magic_link": magic_link}
    send_mail(
        "Votre lien de connexion pour DORA",
        email,
        mjml2html(render_to_string("send_link.mjml", context)),
        from_email=("La plateforme DORA", settings.NO_REPLY_EMAIL),
        tags=["lien-magique"],
    )
