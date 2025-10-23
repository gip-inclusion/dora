# Inspired from https://docs.djangoproject.com/en/3.2/topics/auth/customizing/#a-full-example
import logging
import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone

from ..core.validators import validate_version
from .enums import DiscoveryMethod, MainActivity

logger = logging.getLogger(__name__)

IC_PRODUCTION_DATE = timezone.make_aware(timezone.datetime(2022, 10, 3))


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(email=self.normalize_email(email), **extra_fields)

        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password, **extra_fields)
        user.is_staff = True
        user.save()
        return user

    def normalize_email(self, email):
        """
        Normalise une adresse e-mail en la convertissant en minuscules.

        BaseUserManager.normalize_email() ne convertit que la partie nom
        de domaine de l'adresse. Nous voulons qu'elle soit entièrement
        convertie en minuscules comme le fait la majorité des applications.
        """
        return super().normalize_email(email).lower()

    def get_by_email(self, email):
        normalized_email = self.normalize_email(email)
        return self.get(email=normalized_email)

    def get_dora_bot(self):
        return self.get_by_email(settings.DORA_BOT_USER)

    def orphans(self):
        # utilisateurs sans structure et sans invitation
        return self.filter(putative_membership=None, membership=None, is_staff=False)

    def to_delete(self):
        return self.filter(putative_membership=None).filter(
            is_valid=False, date_joined__lt=IC_PRODUCTION_DATE
        )

    def members_invited(self):
        # invités par un admin de structure, en attente
        return (
            self.exclude(putative_membership=None)
            .filter(putative_membership__invited_by_admin=True)
            .prefetch_related("putative_membership")
        )

    def managers(self):
        return self.filter(is_manager=True)


class User(AbstractBaseUser):
    # null possible en base ... pour l'instant
    sub_pc = models.UUIDField(verbose_name="Identifiant ProConnect", null=True)

    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    last_name = models.CharField("Nom de famille", max_length=140, blank=True)
    first_name = models.CharField("Prénom", max_length=140, blank=True)

    is_active = models.BooleanField(
        "active",
        default=True,
        help_text=(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    is_valid = models.BooleanField(
        "valid",
        default=False,
        help_text="Designates whether this user's email address has been validated.",
    )
    is_staff = models.BooleanField(
        "staff status",
        default=False,
        help_text="Designates whether the user can log into this admin site.",
    )
    is_manager = models.BooleanField(
        "gestionnaire",
        default=False,
        help_text="Indique si l’utilisateur est un gestionnaire (de département)",
    )
    departments = ArrayField(
        base_field=models.CharField(
            max_length=3,
        ),
        blank=True,
        null=True,
        verbose_name="Départements en gestion",
        help_text="Liste des numéros des départements gérés par l'utilisateur (s’il est gestionnaire). Séparés par des virgules.",
    )
    main_activity = models.CharField(
        max_length=25,
        choices=MainActivity.choices,
        verbose_name="Activité principale de l'utilisateur",
        db_index=True,
        blank=True,
    )
    discovery_method = models.CharField(
        max_length=25,
        choices=DiscoveryMethod.choices,
        verbose_name="comment avez-vous connu DORA ?",
        blank=True,
        null=True,
    )
    discovery_method_other = models.CharField(
        max_length=255,
        verbose_name="comment avez-vous connu DORA ? (autre)",
        blank=True,
        null=True,
    )
    date_joined = models.DateTimeField("date joined", default=timezone.now)
    last_service_reminder_email_sent = models.DateTimeField(blank=True, null=True)
    newsletter = models.BooleanField(default=False, db_index=True)

    bookmarks = models.ManyToManyField("services.Service", through="services.Bookmark")

    cgu_versions_accepted = models.JSONField(default=dict)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "utilisateur"
        verbose_name_plural = "utilisateurs"
        abstract = False

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.email:
            self.email = self.__class__.objects.normalize_email(self.email)
        super().save(*args, **kwargs)

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    def get_full_name(self):
        if self.first_name or self.last_name:
            full_name = "%s %s" % (self.first_name, self.last_name)
            return full_name.strip()
        return self.email

    def get_short_name(self):
        return self.first_name or self.last_name or self.email

    def get_safe_name(self):
        # Masque le prénom
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}. {self.last_name}"
        return self.email.split("@")[0]

    def structure_to_join(
        self, siret: str | None = None, safir: str | None = None
    ) -> dict:
        # Pour ProConnect :
        # on cherche à savoir si l'utilisateur est déjà rattaché à l'agence FT ou à la structure donnée.
        # Si on ne trouve aucune invitation ou rattachement, on lui proposera un rattachement lors de
        # la redirection en fin d'identification OIDC.

        if not (safir or siret):
            raise Exception("Aucun SIRET ou SAFIR fourni")

        # Dans le cas d'un SAFIR (prioritaire) :
        if safir:
            # on vérifie si l'utilisateur est membre ou en attente d'invitation sur l'agence FT
            test_safir = (
                self.putative_membership.filter(structure__code_safir_ft=safir)
                .select_related("structure")
                .exists()
                or self.membership.filter(structure__code_safir_ft=safir)
                .select_related("structure")
                .exists()
            )
            return {} if test_safir else {"safir": safir}

        # Dans le cas d'un SIRET :
        if siret:
            # on vérifie si l'utilisateur est membre ou en attente d'invitation sur la structure
            test_siret = (
                self.putative_membership.filter(structure__siret=siret)
                .select_related("structure")
                .exists()
                or self.membership.filter(structure__siret=siret)
                .select_related("structure")
                .exists()
            )
            return {} if test_siret else {"siret": siret}


class ConsentRecord(models.Model):
    """
    Enregistrements de consentement immuables pour la conformité RGPD.
    Chaque action de consentement crée un nouvel enregistrement (jamais de mise à jour).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="consent_records",
        verbose_name="Utilisateur",
    )
    anonymous_user_hash = models.CharField(
        null=True,
        blank=True,
        verbose_name="Identifiant anonyme",
        help_text="userHash du localStorage pour les utilisateurs anonymes",
    )

    consent_version = models.CharField(
        max_length=10,
        verbose_name="Version du consentement",
        help_text="Version de la politique de consentement présentée à l'utilisateur",
        validators=[validate_version],
    )

    consent_choices = models.JSONField(
        default=dict,
        verbose_name="Services consentis",
        help_text="Statut de consentement pour chaque service",
    )

    created_at = models.DateTimeField(
        auto_now_add=True, db_index=True, verbose_name="Date et heure du consentement"
    )

    def save(self, *args, **kwargs):
        if self.anonymous_user_hash == "":
            self.anonymous_user_hash = None
        super().save(*args, **kwargs)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Enregistrement de consentement"
        verbose_name_plural = "Enregistrements de consentement"
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["anonymous_user_hash", "-created_at"]),
        ]
        constraints = [
            models.CheckConstraint(
                check=(
                    models.Q(user__isnull=False, anonymous_user_hash__isnull=True)
                    | models.Q(user__isnull=True, anonymous_user_hash__isnull=False)
                ),
                name="soit_utilisateur_soit_anonyme",
            )
        ]
