import logging

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def send_slack_message(webhook_url: str, text: str):
    """Poste un message sur un Incoming Webhook Slack."""

    if settings.ENVIRONMENT != "production":
        text = f"[{settings.ENVIRONMENT.upper()}] {text}"

    try:
        response = requests.post(
            webhook_url,
            json={"text": text},
            timeout=settings.SLACK_TIMEOUT_SECONDS,
        )
        response.raise_for_status()
    except Exception:
        logger.exception("Slack : échec de l'envoi du message")
