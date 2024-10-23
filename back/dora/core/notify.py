from django.utils import timezone


def send_moderation_notification(entity, user, msg, new_status):
    if new_status != entity.moderation_status:
        msg += f"\nNouveau statut de modération : {new_status.label}"
    entity.log_note(user, msg)
    entity.moderation_status = new_status
    entity.moderation_date = timezone.now()
    entity.save()
