import json

from django.conf import settings
from django.core.files.storage import default_storage
from django.core.mail import EmailMessage


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
