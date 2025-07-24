import json
import re

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage
from django.utils.html import escape
from rest_framework.exceptions import ValidationError


def clean_reply_to(emails):
    # Déduplique et enlève les adresses vides
    if emails:
        return list(set(email for email in emails if email))


def send_mail(
    subject,
    # chaine ou liste de chaines
    to,
    body,
    # soit une chaine, soit un tuple (nom, email)
    from_email=("La plateforme DORA", settings.DEFAULT_FROM_EMAIL),
    tags=None,
    reply_to=None,
    cc=None,
    bcc=None,
    attachments=None,
):
    headers = {
        "X-TM-DOMAIN": settings.EMAIL_DOMAIN,
        "X-TM-TAGS": json.dumps(tags) if tags else "",
        "X-TM-TRACKING": '{"html":{"open":0,"click":0,"text":{"click":0}}}',
        "X-TM-GOOGLEANALYTICS": '{"enable":"0"}',
        "X-TM-TEXTVERSION": 1,
    }

    # Conversion en liste si besoin
    if not isinstance(to, list):
        to = [to]

    if type(from_email) in [list, tuple]:
        name = from_email[0].replace('"', r"\"")
        email = from_email[1]
        from_email = f'"{name}" <{email}>'

    msg = EmailMessage(
        subject,
        body,
        from_email,
        to,
        headers=headers,
        cc=cc,
        bcc=bcc,
        reply_to=clean_reply_to(reply_to),
    )
    msg.content_subtype = "html"
    if attachments is not None:
        for attachment in attachments:
            filename = attachment.split("/")[-1]
            msg.attach(
                filename,
                default_storage.open(attachment).read(),
            )
    try:
        msg.send()
    except Exception:
        raise
    finally:
        if attachments is not None:
            for attachment in attachments:
                default_storage.delete(attachment)


def sanitize_user_input_injected_in_email(user_input, max_length=5000):
    if not user_input:
        return ""

    if len(user_input) > max_length:
        raise ValidationError(f"Message trop long (max {max_length} caractères)")

    dangerous_patterns = [
        r"\{\{.*?\}\}",  # Django templates
        r"\{%.*?%\}",  # Django template tags
        r"<script[^>]*>",  # Script tags
        r"javascript:",  # JavaScript URLs
    ]

    for pattern in dangerous_patterns:
        if re.search(pattern, user_input, re.IGNORECASE | re.DOTALL):
            raise ValidationError("Contenu dangereux détecté dans le message")

    # # Validate only allowed placeholders
    # allowed_placeholders = ["#SERVICE_ADDRESS#"]
    # found_placeholders = re.findall(r"#[A-Z_]+#", user_input)
    #
    # for placeholder in found_placeholders:
    #     if placeholder not in allowed_placeholders:
    #         raise ValidationError(f"Placeholder non autorisé: {placeholder}")

    # Escape HTML
    return escape(user_input)
