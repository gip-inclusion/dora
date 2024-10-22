from django.conf import settings
from django.db import models


class EnumModel(models.Model):
    value = models.CharField(max_length=255, unique=True, db_index=True)
    label = models.CharField(max_length=255)

    class Meta:
        abstract = True

    def __str__(self):
        return self.label


class ModerationStatus(models.TextChoices):
    NEED_INITIAL_MODERATION = (
        "NEED_INITIAL_MODERATION",
        "Première modération nécessaire",
    )
    NEED_NEW_MODERATION = "NEED_NEW_MODERATION", "Nouvelle modération nécessaire"
    IN_PROGRESS = "IN_PROGRESS", "En cours"
    VALIDATED = "VALIDATED", "Validé"


class ModerationMixin(models.Model):
    moderation_status = models.CharField(
        max_length=30,
        choices=ModerationStatus.choices,
        verbose_name="Modération",
        db_index=True,
        null=True,
        blank=True,
    )
    moderation_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        abstract = True


class LogItem(models.Model):
    structure = models.ForeignKey(
        "structures.Structure",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    service = models.ForeignKey(
        "services.Service",
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
    )
    date = models.DateTimeField(auto_now_add=True)
    message = models.TextField()
