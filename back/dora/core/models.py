import uuid

from django.conf import settings
from django.db import models

from dora.users.models import User


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


class ImportJob(models.Model):
    """Tracks the status of CSV imports for monitoring and polling."""

    STATUS_CHOICES = [
        ("pending", "En attente"),
        ("processing", "En cours"),
        ("completed", "Terminé"),
        ("failed", "Échoué"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="import_jobs"
    )
    import_type = models.CharField(
        max_length=50, help_text="Type d'import (services, structures, etc.)"
    )
    filename = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return f"{self.import_type} - {self.filename} ({self.status})"


class ConsentRecord(models.Model):
    """
    Enregistrements de consentement immuables pour la conformité RGPD.
    Chaque action de consentement crée un nouvel enregistrement (jamais de mise à jour).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="consent_records",
        verbose_name="Utilisateur",
    )
    anonymous_id = models.CharField(
        max_length=100,
        db_index=True,
        null=True,
        blank=True,
        verbose_name="Identifiant anonyme",
        help_text="userHash du localStorage pour les utilisateurs anonymes",
    )

    consent_version = models.CharField(
        max_length=10,
        verbose_name="Version du consentement",
        help_text="Version de la politique de consentement présentée à l'utilisateur",
    )

    consent_choices = models.JSONField(
        default=dict,
        verbose_name="Services consentis",
        help_text="Statut de consentement pour chaque service",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date et heure du consentement"
    )

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Enregistrement de consentement"
        verbose_name_plural = "Enregistrements de consentement"
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["anonymous_id", "-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(user__isnull=False, anonymous_id__isnull=True)
                    | models.Q(user__isnull=True, anonymous_id__isnull=False)
                ),
                name="soit_utilisateur_soit_anonyme",
            )
        ]
