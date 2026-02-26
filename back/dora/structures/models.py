import uuid
from typing import Optional

from data_inclusion.schema.v0 import TypologieStructure
from django.conf import settings
from django.contrib.postgres.aggregates import ArrayAgg
from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import (
    BooleanField,
    Case,
    CharField,
    Count,
    Exists,
    F,
    OuterRef,
    Prefetch,
    Q,
    Value,
    When,
)
from django.db.models.functions import Length
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.utils.text import slugify
from itoutils.django.nexus.models import NexusModelMixin, NexusQuerySetMixin

from dora.core.models import EnumModel, LogItem, ModerationMixin, ModerationStatus
from dora.core.utils import code_insee_to_code_dept
from dora.core.validators import (
    validate_accesslibre_url,
    validate_opening_hours_str,
    validate_phone_number,
    validate_safir,
    validate_siret,
)
from dora.decoupage_administratif.utils import get_clean_city_name
from dora.nexus import sync
from dora.sirene.models import Establishment
from dora.sirene.serializers import EstablishmentSerializer
from dora.structures.emails import (
    send_access_granted_notification,
    send_access_rejected_notification,
    send_access_requested_notification,
    send_branch_created_notification,
    send_invitation_accepted_notification,
)
from dora.users.models import User

CharField.register_lookup(Length)


def make_unique_slug(instance, value, length=20):
    model = instance.__class__
    base_slug = slugify(value)[:length]
    unique_slug = base_slug
    while model.objects.filter(slug=unique_slug).exists():
        unique_slug = (
            base_slug + "-" + get_random_string(4, "abcdefghijklmnopqrstuvwxyz")
        )
    return unique_slug


class StructurePutativeMemberQuerySet(models.QuerySet):
    def invited_by_admin(self):
        # essentiellement pour notifications
        return self.filter(
            invited_by_admin=True,
            user__is_staff=False,
        ).select_related("user", "structure")

        # cat 1 : user__is_valid = True
        # cat 2 : user__is_valid = False


class StructurePutativeMember(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="putative_membership",
    )
    structure = models.ForeignKey(
        "Structure", on_delete=models.CASCADE, related_name="putative_membership"
    )
    is_admin = models.BooleanField(default=False)
    creation_date = models.DateTimeField(auto_now_add=True)

    invited_by_admin = models.BooleanField(default=False)

    objects = StructurePutativeMemberQuerySet.as_manager()

    class Meta:
        verbose_name = "Membre Potentiel"
        verbose_name_plural = "Membres Potentiels"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "structure"],
                name="%(app_label)s_unique_putative_member_by_structure",
            )
        ]

    def __str__(self):
        return self.user.get_full_name()

    def notify_admin_access_requested(self):
        structure_admins = StructureMember.objects.filter(
            structure=self.structure, is_admin=True
        ).exclude(user=self.user)
        for admin in structure_admins:
            send_access_requested_notification(self, admin.user)

    def notify_access_rejected(self):
        send_access_rejected_notification(self)


class StructureMemberQuerySet(NexusQuerySetMixin, models.QuerySet):
    def _get_nexus_queryset(self):
        return super()._get_nexus_queryset().select_related("structure", "user")


class StructureMember(NexusModelMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="membership"
    )
    structure = models.ForeignKey(
        "Structure", on_delete=models.CASCADE, related_name="membership"
    )
    is_admin = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)

    objects = models.Manager.from_queryset(StructureMemberQuerySet)()

    class Meta:
        verbose_name = "Membre"
        constraints = [
            models.UniqueConstraint(
                fields=["user", "structure"],
                name="%(app_label)s_unique_user_by_structure",
            )
        ]

    nexus_tracked_fields = sync.MEMBERSHIP_TRACKED_FIELDS
    nexus_sync = staticmethod(sync.sync_memberships)
    nexus_delete = staticmethod(sync.delete_memberships)

    def should_sync_to_nexus(self):
        return (
            self.user.should_sync_to_nexus() and self.structure.should_sync_to_nexus()
        )

    def __str__(self):
        return self.user.get_full_name()

    def notify_admins_invitation_accepted(self):
        structure_admins = StructureMember.objects.filter(
            structure=self.structure, is_admin=True
        ).exclude(user=self.user)
        for admin in structure_admins:
            send_invitation_accepted_notification(self, admin.user)

    def notify_access_granted(self):
        send_access_granted_notification(self)


class StructureSource(EnumModel):
    class Meta:
        verbose_name = "Source"


class StructureNationalLabel(EnumModel):
    class Meta:
        verbose_name = "Label national"
        verbose_name_plural = "Labels nationaux"


class StructureQuerySet(NexusQuerySetMixin, models.QuerySet):
    def orphans(self):
        return self.filter(membership=None, putative_membership=None)

    def annotated_structures_for_admin(self):
        from dora.services.enums import ServiceStatus
        from dora.services.models import Service

        return self.prefetch_related(
            "national_labels",
            Prefetch(
                "putative_membership",
                queryset=StructurePutativeMember.objects.filter(
                    user__is_active=True
                ).select_related("user"),
                to_attr="potential_members",
            ),
        ).annotate(
            num_draft_services=Count(
                "services",
                distinct=True,
                filter=Q(services__status=ServiceStatus.DRAFT),
            ),
            num_published_services=Count(
                "services",
                distinct=True,
                filter=Q(services__status=ServiceStatus.PUBLISHED),
            ),
            num_active_services=Count(
                "services",
                distinct=True,
                filter=~Q(services__status=ServiceStatus.ARCHIVED),
            ),
            num_outdated_services=Service.objects.update_advised()
            .filter(structure=OuterRef("pk"))
            .values("structure")
            .annotate(count=Count("*"))
            .values("count")[:1],
            has_valid_admin=Exists(
                StructureMember.objects.filter(
                    structure=OuterRef("pk"),
                    is_admin=True,
                    user__is_valid=True,
                    user__is_active=True,
                )
            ),
            is_orphan=Case(
                When(
                    Exists(StructureMember.objects.filter(structure=OuterRef("pk")))
                    | Exists(
                        StructurePutativeMember.objects.filter(structure=OuterRef("pk"))
                    ),
                    then=Value(False),
                ),
                default=Value(True),
                output_field=BooleanField(),
            ),
            awaiting_moderation=Case(
                When(
                    moderation_status__in=[
                        ModerationStatus.NEED_NEW_MODERATION,
                        ModerationStatus.NEED_INITIAL_MODERATION,
                    ],
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            is_waiting=Case(
                When(
                    ~Exists(
                        StructureMember.objects.filter(
                            structure=OuterRef("pk"),
                            is_admin=True,
                            user__is_valid=True,
                            user__is_active=True,
                        )
                    )
                    & Exists(
                        StructurePutativeMember.objects.filter(
                            structure=OuterRef("pk"),
                            is_admin=True,
                            invited_by_admin=True,
                            user__is_active=True,
                        )
                    ),
                    then=Value(True),
                ),
                default=Value(False),
                output_field=BooleanField(),
            ),
            categories_list=ArrayAgg(
                "services__categories__value",
                distinct=True,
                filter=Q(services__categories__isnull=False),
            ),
            admin_emails=ArrayAgg(
                "membership__user__email",
                distinct=True,
                filter=Q(
                    membership__is_admin=True,
                    membership__user__is_valid=True,
                    membership__user__is_active=True,
                ),
            ),
            editor_emails=ArrayAgg(
                "services__last_editor__email",
                distinct=True,
                filter=Q(
                    ~Q(services__last_editor__email=settings.DORA_BOT_USER),
                    services__status=ServiceStatus.PUBLISHED,
                    services__last_editor__isnull=False,
                ),
            ),
        )

    def orphans_for_manager(self, manager: User):
        return self.orphans().filter(department__in=manager.departments)

    def awaiting_moderation(self, manager: User | None = None):
        queryset = self.annotated_structures_for_admin().filter(is_obsolete=False)
        if manager:
            queryset = queryset.filter(department__in=manager.departments)
        return queryset.filter(
            is_orphan=False, is_waiting=False, awaiting_moderation=True
        )

    def requiring_action_from_department_managers(self):
        return self.orphans() | self.awaiting_moderation()


class StructureManager(models.Manager):
    def create_from_establishment(
        self, establishment, name="", parent=None, structure_id=None, **kwargs
    ):
        data = EstablishmentSerializer(establishment).data
        siret = data["siret"]
        structure = self.model(
            siret=siret if not parent or parent.siret != siret else None,
            parent=parent,
            name=name if name else data["name"],
            address1=data["address1"],
            address2=data["address2"],
            postal_code=data["postal_code"],
            city_code=data["city_code"],
            city=data["city"],
            ape=data["ape"],
            longitude=data["longitude"],
            latitude=data["latitude"],
            modification_date=timezone.now(),
            **kwargs,
        )
        if structure_id:
            structure.id = structure_id
        structure.save()
        return structure


StructureManager = StructureManager.from_queryset(StructureQuerySet)


class Structure(NexusModelMixin, ModerationMixin, models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # Les antennes peuvent avoir un Siret null
    siret = models.CharField(
        verbose_name="SIRET",
        max_length=14,
        validators=[validate_siret],
        blank=True,
        null=True,
        unique=True,
    )
    parent = models.ForeignKey(
        "self", on_delete=models.CASCADE, blank=True, null=True, related_name="branches"
    )

    code_safir_ft = models.CharField(
        verbose_name="code SAFIR France Travail",
        max_length=5,
        validators=[validate_safir],
        unique=True,
        null=True,
        blank=True,
        db_index=True,
    )

    name = models.CharField(verbose_name="Nom", max_length=255, db_index=True)

    typology = models.CharField(
        choices=zip(
            [t.value for t in TypologieStructure], [t.label for t in TypologieStructure]
        ),
        max_length=100,
        default="",
    )
    slug = models.SlugField(blank=True, null=True, unique=True)
    url = models.URLField(blank=True)
    short_desc = models.CharField(max_length=280, blank=True)
    full_desc = models.TextField(blank=True)
    phone = models.CharField(
        max_length=10, blank=True, validators=[validate_phone_number]
    )
    email = models.EmailField(blank=True)
    address1 = models.CharField(max_length=255, blank=True)
    address2 = models.CharField(max_length=255, blank=True)
    postal_code = models.CharField(max_length=5, blank=True)
    city_code = models.CharField(max_length=5, blank=True)
    # lecture seule
    city = models.CharField(max_length=255, blank=True)
    department = models.CharField(max_length=3, blank=True)
    #
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    # valeur indiquant la pertinence des valeurs lat/lon issues d'un géocodage
    # valeur allant de 0 (pas pertinent) à 1 (pertinent)
    geocoding_score = models.FloatField(blank=True, null=True)

    ape = models.CharField(max_length=6, blank=True)

    accesslibre_url = models.URLField(
        verbose_name="URL accesslibre",
        blank=True,
        null=True,
        validators=[validate_accesslibre_url],
    )
    opening_hours = models.CharField(
        max_length=255, blank=True, null=True, validators=[validate_opening_hours_str]
    )
    opening_hours_details = models.CharField(max_length=255, blank=True, null=True)
    national_labels = models.ManyToManyField(StructureNationalLabel, blank=True)
    other_labels = ArrayField(
        models.TextField(),
        blank=True,
        default=list,
    )
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(blank=True, null=True)
    has_been_edited = models.BooleanField(default=False)
    quick_start_done = models.BooleanField(default=False)
    creator = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="+",
    )
    last_editor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        related_name="+",
        blank=True,
        null=True,
    )

    source = models.ForeignKey(
        StructureSource, null=True, blank=True, on_delete=models.PROTECT
    )
    data_inclusion_id = models.TextField(blank=True, db_index=True)
    data_inclusion_source = models.TextField(blank=True, db_index=True)

    members = models.ManyToManyField(User, through=StructureMember)
    putative_members = models.ManyToManyField(
        User, through=StructurePutativeMember, related_name="putative_structure_set"
    )

    disable_orientation_form = models.BooleanField(default=False)

    is_obsolete = models.BooleanField(default=False, db_index=True)

    admin_already_invited = models.BooleanField(default=False)

    objects = StructureManager()

    class Meta:
        constraints = [
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_valid_or_null_siren",
                condition=Q(siret__length=14) | Q(siret__isnull=True),
            ),
            models.CheckConstraint(
                name="%(app_label)s_%(class)s_null_siret_only_in_branches",
                condition=Q(siret__isnull=False) | Q(parent__isnull=False),
            ),
        ]

    nexus_tracked_fields = sync.STRUCTURE_TRACKED_FIELDS
    nexus_sync = staticmethod(sync.sync_structues)
    nexus_delete = staticmethod(sync.delete_structures)

    def clean(self):
        if not (self.siret is not None or self.parent is not None):
            raise ValidationError("Seules les antennes peuvent avoir un siret vide")
        if self.siret is not None:
            try:
                Establishment.objects.get(siret=self.siret)
            except Establishment.DoesNotExist:
                raise ValidationError("SIRET invalide")
            if self.parent and self.siret[:9] != self.parent.siret[:9]:
                raise ValidationError(
                    f"Le SIREN {self.siret[:9]}  est different de celui de la structure mère {self.parent.siret[:9]}"
                )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return self.get_frontend_url()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = make_unique_slug(self, self.name)
        if self.city_code:
            self.department = code_insee_to_code_dept(self.city_code)
            self.city = get_clean_city_name(self.city_code)
        return super().save(*args, **kwargs)

    def should_sync_to_nexus(self):
        return not self.is_obsolete and "[ND]" not in self.name

    def can_edit_informations(self, user: User):
        return user.is_authenticated and (
            user.is_staff or self.is_manager(user) or self.is_admin(user)
        )

    def can_view_members(self, user: User):
        return user.is_authenticated and (
            user.is_staff or self.is_manager(user) or self.is_member(user)
        )

    def can_edit_members(self, user: User):
        return user.is_authenticated and (
            user.is_staff or self.is_admin(user) or self.is_manager(user)
        )

    def can_edit_services(self, user: User):
        return user.is_authenticated and (
            user.is_staff or self.is_manager(user) or self.is_member(user)
        )

    def is_member(self, user):
        return StructureMember.objects.filter(
            structure_id=self.id, user_id=user.id
        ).exists()

    def is_admin(self, user):
        return StructureMember.objects.filter(
            structure_id=self.id, user_id=user.id, is_admin=True
        ).exists()

    def is_manager(self, user: User):
        return (
            user.is_authenticated
            and user.is_manager
            and user.departments
            and self.department in user.departments
        )

    @property
    def admins(self):
        return [
            m.user
            for m in self.membership.filter(
                is_admin=True, user__is_valid=True, user__is_active=True
            )
        ]

    def has_admin(self):
        return bool(self.num_admins())

    def num_admins(self):
        return len(self.admins)

    def is_pending_member(self, user):
        return StructurePutativeMember.objects.filter(
            structure_id=self.id, user_id=user.id, invited_by_admin=False
        ).exists()

    def post_create_branch(self, branch, user, source):
        branch.creator = user
        branch.last_editor = user
        branch.source = source
        branch.modification_date = timezone.now()
        branch.moderation_status = ModerationStatus.VALIDATED
        branch.moderation_date = timezone.now()
        branch.save()
        structure_admins = StructureMember.objects.filter(structure=self, is_admin=True)
        for admin in structure_admins:
            StructureMember.objects.create(
                structure=branch, is_admin=True, user=admin.user
            )
            send_branch_created_notification(self, branch, admin.user)

    def fill_contact(
        self,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        url: Optional[str] = None,
    ):
        """Complète les informations de contact"""
        self.email = self.email or email or ""
        self.phone = self.phone or phone or ""
        self.url = self.url or url or ""
        self.save(update_fields=["email", "phone", "url"])

    def get_num_visible_services(self, user):
        if user.is_authenticated and (
            user.is_staff or self.is_manager(user) or self.is_member(user)
        ):
            return self.services.active().count()
        else:
            return self.services.published().count()

    def get_num_visible_models(self, user):
        # On ne peut pas utiliser le manager lié (self.services) étant donné qu'il filtre les modèles
        from dora.services.models import ServiceModel

        return ServiceModel.objects.filter(structure=self).count()

    def get_frontend_url(self):
        return f"{settings.FRONTEND_URL}/structures/{self.slug}"

    def get_admin_url(self):
        return (
            f"https://{settings.ALLOWED_HOSTS[0]}/structures/structure/{self.id}/change"
        )

    def log_note(self, user, msg):
        LogItem.objects.create(structure=self, user=user, message=msg.strip())

    def get_most_recently_active_admin(self):
        return (
            StructureMember.objects.filter(
                structure_id=self.id,
                user__is_active=True,
                user__is_valid=True,
                is_admin=True,
            )
            .order_by(F("user__last_login").desc(nulls_last=True))
            .first()
        )

    def no_dora_form(self):
        siren = self.siret[:9] if self.siret else None
        return siren in settings.ORIENTATION_SIRENE_BLACKLIST


class DisabledDoraFormDIStructure(models.Model):
    class Meta:
        verbose_name = "structure DI avec formulaire Dora désactivé"
        verbose_name_plural = "structures DI avec formulaire Dora désactivé"

    source = models.CharField(
        verbose_name="Source",
        max_length=255,
    )
    structure_id = models.CharField(
        verbose_name="ID de la structure",
        max_length=1024,
    )
    comment = models.TextField(verbose_name="Commentaire", blank=True)
