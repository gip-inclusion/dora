import hashlib

from django.contrib.gis.geos import Point
from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone

from dora.admin_express.models import AdminDivisionType
from dora.admin_express.utils import arrdt_to_main_insee_code
from dora.core.constants import WGS84
from dora.core.models import ModerationStatus
from dora.decoupage_administratif.models import EPCI, City, Department, Region
from dora.services.enums import ServiceStatus

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
    "online_form",
    "qpv_or_zrr",
    "recurrence",
    "suspension_date",
]

# Many to many fields
SYNC_M2M_FIELDS = [
    "kinds",
    "categories",
    "subcategories",
    "beneficiaries_access_modes",
    "coach_orientation_modes",
]

# Custom Many to many fields
SYNC_CUSTOM_M2M_FIELDS = [
    "access_conditions",
    "publics",
    "requirements",
    "credentials",
]


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

    return service


def update_sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        md5.update(repr(getattr(service, field)).encode())
    for m2m_field in [*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS]:
        md5.update(
            repr(
                list(
                    getattr(service, m2m_field)
                    .all()
                    .values_list("pk", flat=True)
                    .order_by("pk")
                )
            ).encode()
        )

    result = md5.hexdigest()
    return result


def filter_services_by_city_code(services, city_code):
    # Si la requete entrante contient un code insee d'arrondissement,
    # on le convertit pour récupérer le code de la commune entière.
    city_code = arrdt_to_main_insee_code(city_code)
    city = get_object_or_404(City, pk=city_code)

    return services.filter(
        Q(diffusion_zone_type=AdminDivisionType.COUNTRY)
        | (
            Q(diffusion_zone_type=AdminDivisionType.CITY)
            & Q(diffusion_zone_details=city.code)
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.EPCI)
            & Q(diffusion_zone_details=city.epci)
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.DEPARTMENT)
            & Q(diffusion_zone_details=city.department)
        )
        | (
            Q(diffusion_zone_type=AdminDivisionType.REGION)
            & Q(diffusion_zone_details=city.region)
        )
    )


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
