import hashlib

from data_inclusion.schema.v1 import TypeService
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.contrib.gis.geos import Point
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from dora.core.constants import WGS84
from dora.core.models import ModerationStatus
from dora.decoupage_administratif.models import (
    EPCI,
    AdminDivisionType,
    City,
    Department,
    Region,
)
from dora.services.enums import ServiceStatus
from dora.services.mobilisation import sync_mobilisation_fields

SYNC_FIELDS = [
    "name",
    "short_desc",
    "full_desc",
    "is_cumulative",
    "fee_condition",
    "fee_details",
    "beneficiaries_access_modes_external_form_link",
    "beneficiaries_access_modes_external_form_link_text",
    "beneficiaries_access_modes_other",
    "coach_orientation_modes_external_form_link",
    "coach_orientation_modes_external_form_link_text",
    "coach_orientation_modes_other",
    "duration_weekly_hours",
    "duration_weeks",
    "forms",
    "kind",
    "online_form",
    "publics",
    "publics_precisions",
    "qpv_or_zrr",
    "recurrence",
    "suspension_date",
]

# Clés étrangères parmi `SYNC_FIELDS` : hachées par leur identifiant plutôt que par
# l'instance liée, dont le `repr()` dépend du `__str__` — inexistant sur les modèles
# historiques d'une migration, et qui changerait l'empreinte de tous les modèles au moindre
# renommage d'un libellé.
SYNC_FK_FIELDS = {"fee_condition"}

# Many to many fields
SYNC_M2M_FIELDS = [
    "categories",
    "subcategories",
    "beneficiaries_access_modes",
    "coach_orientation_modes",
]

# Custom Many to many fields
SYNC_CUSTOM_M2M_FIELDS = [
    "access_conditions",
    "requirements",
    "credentials",
]

TOUS_PUBLICS = DiPublic.TOUS_PUBLICS.value
VALID_DI_PUBLICS = {p.value for p in DiPublic}

# Ordre de référence des publics DI : `publics` est normalisé à l'écriture selon cet
# ordre (cf. `ServiceSerializer.validate`) afin que la composition, et non l'ordre de
# saisie, détermine l'empreinte de synchronisation, l'historique de modification et le
# diff « modèle modifié » côté front. On suit l'ordre du référentiel plutôt que l'ordre
# alphabétique pour rester aligné sur l'affichage des libellés (`get_publics_display`).
DI_PUBLICS_ORDER = {p.value: index for index, p in enumerate(DiPublic)}


def normalize_publics(publics):
    return sorted(set(publics), key=DI_PUBLICS_ORDER.__getitem__)


def _duplicate_customizable_choices(field, choices, structure):
    for choice in choices:
        if choice.structure:
            new_choice, _created = choice._meta.model.objects.get_or_create(
                name=choice.name, structure=structure
            )
            field.add(new_choice)
        else:
            field.add(choice)


def instantiate_service_from_model(model, structure, user):
    service = model.__class__.objects.create(structure=structure)

    for field in SYNC_FIELDS:
        setattr(service, field, getattr(model, field))

    # Mettre l'adresse de la structure au lieu d'utiliser celle du modèle
    service.address1 = structure.address1
    service.address2 = structure.address2
    service.postal_code = structure.postal_code
    service.city_code = structure.city_code
    service.city = structure.city
    if structure.longitude and structure.latitude:
        service.geom = Point(structure.longitude, structure.latitude, srid=WGS84)
    else:
        service.geom = None

    # Metadata
    service.is_model = False
    service.creator = model.creator
    service.last_editor = user
    service.model = model
    service.last_sync_checksum = model.sync_checksum
    service.modification_date = timezone.now()
    service.moderation_status = ModerationStatus.VALIDATED
    service.moderation_date = timezone.now()
    service.status = ServiceStatus.DRAFT

    # Restaure les champs M2M
    for field in SYNC_M2M_FIELDS:
        getattr(service, field).set(getattr(model, field).all())

    for field in SYNC_CUSTOM_M2M_FIELDS:
        _duplicate_customizable_choices(
            getattr(service, field), getattr(model, field).all(), service.structure
        )

    service.save()
    sync_mobilisation_fields(service)
    return service


def synchronize_service_from_model(service, model):
    for field in SYNC_FIELDS:
        setattr(service, field, getattr(model, field))

    for field in SYNC_M2M_FIELDS:
        getattr(service, field).set(getattr(model, field).all())

    for field in SYNC_CUSTOM_M2M_FIELDS:
        _duplicate_customizable_choices(
            getattr(service, field), getattr(model, field).all(), service.structure
        )

    sync_mobilisation_fields(service)
    return service


def update_sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        attr = f"{field}_id" if field in SYNC_FK_FIELDS else field
        value = getattr(service, attr)
        md5.update(repr(value).encode())
    for m2m_field in [*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS]:
        # `.all()` sert le cache de `prefetch_related` quand il existe, là où un
        # `.values_list()` reclone le queryset et repart en base à chaque champ.
        pks = sorted(obj.pk for obj in getattr(service, m2m_field).all())
        md5.update(repr(pks).encode())

    result = md5.hexdigest()
    return result


def filter_services_by_department(services, dept_code):
    department = get_object_or_404(Department, pk=dept_code)

    return services.filter(
        Q(diffusion_zone_type=AdminDivisionType.COUNTRY)
        | (
            Q(diffusion_zone_type=AdminDivisionType.CITY)
            & Q(diffusion_zone_details__in=City.objects.filter(department=dept_code))
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.EPCI)
            & Q(
                diffusion_zone_details__in=EPCI.objects.filter(
                    departments__contains=[dept_code]
                )
            )
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.DEPARTMENT)
            & Q(diffusion_zone_details=department.code)
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.REGION)
            & Q(diffusion_zone_details=department.region)
        )
    )


def filter_services_by_region(services, region_code):
    region = get_object_or_404(Region, pk=region_code)

    return services.filter(
        Q(diffusion_zone_type=AdminDivisionType.COUNTRY)
        | (
            Q(diffusion_zone_type=AdminDivisionType.CITY)
            & Q(diffusion_zone_details__in=City.objects.filter(region=region_code))
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.EPCI)
            & Q(
                diffusion_zone_details__in=EPCI.objects.filter(
                    regions__contains=[region_code]
                )
            )
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.DEPARTMENT)
            & Q(
                diffusion_zone_details__in=Department.objects.filter(region=region_code)
            )
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.REGION)
            & Q(diffusion_zone_details=region.code)
        )
    )


def get_kinds_labels(kinds):
    return [TypeService(kind).label for kind in kinds]
