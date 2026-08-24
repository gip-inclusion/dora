from django.conf import settings

from dora.core.slack import send_slack_message


def send_orientation_moderation_pending_notification(orientation):
    """Prévient l'équipe qu'une orientation attend la modération de sa structure émettrice."""
    structure = orientation.prescriber_structure

    send_slack_message(
        settings.SLACK_MODERATION_WEBHOOK_URL,
        "🔔 Nouvelle orientation en attente de modération\n"
        f"Structure : « {structure.name} »\n"
        f"Modérer : {structure.get_admin_url()}",
    )
