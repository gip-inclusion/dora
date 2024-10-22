from django.db import models


class NotificationStatus(models.TextChoices):
    PENDING = "pending"
    COMPLETE = "complete"
    EXPIRED = "expired"


class TaskType(models.TextChoices):
    ORPHAN_STRUCTURES = "orphan_structures"
    SERVICE_ACTIVATION = "service_activation"
    INVITED_USERS = "invited_users"
    SELF_INVITED_USERS = "self_invited_users"
    USERS_WITHOUT_STRUCTURE = "users_without_structure"
    USER_ACCOUNT_DELETION = "user_account_deletion"

    ...

    # catch-all: pour des cas de tests, ou "one-shot"
    GENERIC_TASK = "generic_task"
