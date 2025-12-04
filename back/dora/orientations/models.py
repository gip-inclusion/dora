import hashlib
import logging
import uuid

from dateutil.relativedelta import relativedelta
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.core.files.storage import default_storage
from django.db import models
from django.utils import timezone

from dora.core.models import EnumModel
from dora.services.models import Service
from dora.structures.models import Structure

ORIENTATION_QUERY_LINK_TTL_DAY = 8

logger = logging.getLogger("dora.logs.core")


class ContactPreference(models.TextChoices):
    PHONE = "TELEPHONE", "Téléphone"
    EMAIL = "EMAIL", "E-mail"
    REFERENT = "REFERENT", "Via le conseiller référent"
    OTHER = "AUTRE", "Autre"


class OrientationStatus(models.TextChoices):
    MODERATION_PENDING = "MODÉRATION_EN_COURS", "En cours de modération"
    MODERATION_REJECTED = "MODÉRATION_REJETÉE", "Rejetée par la modération"
    PENDING = "OUVERTE", "Ouverte / En cours de traitement"
    ACCEPTED = "VALIDÉE", "Validée"
    REJECTED = "REFUSÉE", "Refusée"
    EXPIRED = "EXPIRÉE", "Expirée"


class RejectionReason(EnumModel):
    class Meta:
        verbose_name = "Motif de refus"
        verbose_name_plural = "Motifs de refus"


def _orientation_query_expiration_date():
    # lu quelque part: les lambdas sont moyennement appréciées dans les migrations
    return timezone.now() + relativedelta(days=ORIENTATION_QUERY_LINK_TTL_DAY)


class Orientation(models.Model):
    id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name="ID",
    )

    query_id = models.UUIDField(default=uuid.uuid4, editable=False, db_index=True)

    query_expires_at = models.DateTimeField(
        default=_orientation_query_expiration_date,
        verbose_name="expiration du lien de la demande",
    )

    # Infos bénéficiaires
    requirements = ArrayField(
        models.CharField(max_length=480),
        verbose_name="Critères",
        blank=True,
        default=list,
    )
    situation = ArrayField(
        models.CharField(max_length=480),
        verbose_name="Situation",
        blank=True,
        default=list,
    )
    situation_other = models.CharField(
        max_length=480, verbose_name="Situation - autre", blank=True
    )

    beneficiary_france_travail_number = models.CharField(
        max_length=11, verbose_name="Numéro France Travail", blank=True
    )

    beneficiary_last_name = models.CharField(
        max_length=140, verbose_name="Nom bénéficiaire"
    )
    beneficiary_first_name = models.CharField(
        max_length=140, verbose_name="Prénom bénéficiaire"
    )

    beneficiary_contact_preferences = ArrayField(
        models.CharField(
            choices=ContactPreference.choices,
            max_length=10,
            blank=True,
        ),
        verbose_name="Préférences de contact",
        default=list,
    )

    beneficiary_phone = models.CharField(
        verbose_name="Tel bénéficiaire", max_length=10, blank=True
    )
    beneficiary_email = models.EmailField(
        verbose_name="Courriel bénéficiaire", blank=True
    )
    beneficiary_other_contact_method = models.CharField(
        verbose_name="Autre méthode de contact bénéficiaire", max_length=280, blank=True
    )
    beneficiary_availability = models.DateField(
        verbose_name="Disponibilité bénéficiaire", blank=True, null=True
    )

    beneficiary_attachments = ArrayField(
        models.CharField(max_length=1024),
        verbose_name="Documents joints",
        blank=True,
        default=list,
    )

    # Infos du référent
    referent_last_name = models.CharField(max_length=140, verbose_name="Nom référent")
    referent_first_name = models.CharField(
        max_length=140, verbose_name="Prénom référent"
    )
    referent_phone = models.CharField(
        verbose_name="Tel référent", max_length=10, blank=True
    )
    referent_email = models.EmailField(verbose_name="Courriel référent")

    # Durée du service
    duration_weekly_hours = models.PositiveIntegerField(
        verbose_name="Nombre d'heures par semaine",
        help_text="Nombre d'heures par semaine pour effectuer ce service",
        blank=True,
        null=True,
    )
    duration_weeks = models.PositiveIntegerField(
        verbose_name="Nombre de semaines",
        help_text="Nombre de semaines que durent le service",
        blank=True,
        null=True,
    )

    # Meta
    prescriber = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name="Prescripteur",
        on_delete=models.SET_NULL,
        null=True,
    )
    prescriber_structure = models.ForeignKey(
        Structure,
        verbose_name="Structure",
        on_delete=models.SET_NULL,
        related_name="orientations",
        null=True,
    )
    service = models.ForeignKey(
        Service,
        verbose_name="Service",
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    di_service_id = models.TextField(blank=True, default="")
    di_service_name = models.TextField(blank=True, default="")
    di_service_address_line = models.TextField(blank=True, default="")
    di_contact_email = models.TextField(blank=True, default="")
    di_contact_name = models.TextField(blank=True, default="")
    di_contact_phone = models.TextField(blank=True, default="")
    di_structure_name = models.TextField(blank=True, default="")

    data_protection_commitment = models.BooleanField(
        verbose_name="Engagement RGPD accompagnateur", default=False
    )

    original_service_name = models.CharField(
        verbose_name="Nom original", max_length=140, default="", editable=False
    )
    orientation_reasons = models.TextField(
        verbose_name="Motif de l'orientation", blank=True
    )
    rejection_reasons = models.ManyToManyField(
        RejectionReason, verbose_name="Motifs de refus de l'orientation", blank=True
    )

    creation_date = models.DateTimeField(
        auto_now_add=True, editable=False, verbose_name="date de création"
    )
    processing_date = models.DateTimeField(
        blank=True, null=True, verbose_name="date de traitement"
    )
    status = models.CharField(
        max_length=20,
        choices=OrientationStatus.choices,
        default=OrientationStatus.PENDING,
        verbose_name="statut",
    )
    last_reminder_email_sent = models.DateTimeField(blank=True, null=True)

    class Meta:
        constraints = (
            # service lié à l'orientation : DORA ou D·I, mais pas les deux
            models.CheckConstraint(
                condition=(
                    (models.Q(service=None) & ~models.Q(di_service_id=""))
                    | (~models.Q(service=None) & models.Q(di_service_id=""))
                ),
                name="check_valid_service",
            ),
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._original_status = self.status

    def save(self, *args, **kwargs):
        if not self.id:
            self.original_service_name = self.get_service_name()

        if self.pk and self.status != self._original_status:
            self.processing_date = timezone.now()
            self._original_status = self.status

        result = super().save(*args, **kwargs)

        return result

    def delete(self, *args, **kwargs):
        if self.beneficiary_attachments:
            self.delete_attachments()
        super().delete(*args, **kwargs)

    def __str__(self):
        return f"Orientation #{self.id}"

    def get_query_id_hash(self) -> str:
        return hashlib.sha256(
            f"{self.query_id}{self.query_expires_at}{settings.SECRET_KEY}".encode(
                "utf8"
            )
        ).hexdigest()

    def get_magic_link(self):
        return f"{settings.FRONTEND_URL}/orientations?token={self.query_id}&h={self.get_query_id_hash()}"

    def get_absolute_url(self):
        # utilisé seulement par la fonctionnalité `view_on_site` de l'admin :
        # doit retourner l'URL "magique"
        return self.get_magic_link()

    def get_frontend_url(self):
        return f"{settings.FRONTEND_URL}/orientations?token={self.query_id}"

    def get_beneficiary_full_name(self):
        if self.beneficiary_first_name or self.beneficiary_last_name:
            full_name = "%s %s" % (
                self.beneficiary_first_name,
                self.beneficiary_last_name,
            )
            return full_name.strip()
        return self.beneficiary_email

    def get_referent_full_name(self):
        if self.referent_first_name or self.referent_last_name:
            full_name = "%s %s" % (
                self.referent_first_name,
                self.referent_last_name,
            )
            return full_name.strip()
        return self.referent_email

    # Permet de renvoyer au besoin les valeurs dora ou d·i
    def get_service_name(self):
        return (
            self.service.name
            if self.service
            else self.di_service_name
            if self.di_service_id
            else self.original_service_name
        )

    def get_service_address_line(self):
        return (
            self.service.address_line()
            if self.service
            else self.di_service_address_line
            if self.di_service_id
            else ""
        )

    def get_contact_email(self):
        return (
            self.service.contact_email
            if self.service
            else self.di_contact_email
            if self.di_service_id
            else ""
        )

    def get_contact_name(self):
        return (
            self.service.contact_name
            if self.service
            else self.di_contact_name
            if self.di_service_id
            else ""
        )

    def get_contact_phone(self):
        return (
            self.service.contact_phone
            if self.service
            else self.di_contact_phone
            if self.di_service_id
            else ""
        )

    def get_structure_name(self):
        return (
            self.service.structure.name
            if self.service
            else self.di_structure_name
            if self.di_service_id
            else ""
        )

    def get_structure_frontend_url(self):
        return self.service.structure.get_frontend_url() if self.service else ""

    def get_service_frontend_url(self):
        if self.service:
            return self.service.get_frontend_url()
        elif self.di_service_id:
            return f"{settings.FRONTEND_URL}/services/di--{self.di_service_id}"
        else:
            return ""

    def refresh_query_expiration_date(self):
        # on ne régénère le lien que si il est expiré
        if self.query_expired:
            self.query_expires_at = _orientation_query_expiration_date()
            self.save()
            logger.info(
                "orientation:refresh_link",
                {
                    "legal": True,
                    "reason": "lien expiré",
                    "queryId": str(self.query_id),
                    "ttlInDays": ORIENTATION_QUERY_LINK_TTL_DAY,
                },
            )

    def delete_attachment(self, attachment: str) -> (str, bool):
        # Détruit une pièce-jointe de l'orientation, *si elle existe*.
        if default_storage.exists(attachment):
            default_storage.delete(attachment)
            logger.info("deleteOrientationAttachment", {"path": attachment})
            self.beneficiary_attachments.remove(attachment)
            self.save()
            return attachment, True
        else:
            logger.warning("deleteOrientationAttachment", {"pathNotFound": attachment})
            return attachment, False

    def delete_attachments(self) -> dict[str, bool]:
        # Cette méthode effectue des appels synchrones via `django-storages` pour la destruction
        # des pièces-jointes de l'orientation concernée.
        # Elle ne devrait idéalement être utilisée que via des management-commands ou en shell.
        return dict(
            self.delete_attachment(attachment)
            for attachment in list(
                self.beneficiary_attachments
            )  # ne pas oublier la copie...
        )

    @property
    def query_expired(self) -> bool:
        return timezone.now() > self.query_expires_at


class ContactRecipient(models.TextChoices):
    BENEFICIARY = "BÉNÉFICIAIRE", "Bénéficiaire"
    PRESCRIBER = "PRESCRIPTEUR", "Prescripteur"
    REFERENT = "RÉFÉRENT", "Référent"


class SentContactEmail(models.Model):
    orientation = models.ForeignKey(
        Orientation,
        on_delete=models.CASCADE,
    )
    date_sent = models.DateTimeField(auto_now_add=True, editable=False)
    recipient = models.CharField(
        choices=ContactRecipient.choices,
        max_length=20,
    )
    carbon_copies = ArrayField(
        models.CharField(
            choices=ContactRecipient.choices,
            max_length=20,
        ),
        verbose_name="Carbon Copies",
        blank=True,
        default=list,
    )
