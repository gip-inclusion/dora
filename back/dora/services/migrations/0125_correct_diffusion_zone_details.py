import logging

from django.conf import settings
from django.db import migrations
from django.db.models import Q
from django.utils import timezone

from dora.admin_express.models import AdminDivisionType

logger = logging.getLogger(__name__)


def get_department_for_service(service):
    logger.info(f"Mise à jour du service avec l'id {service.id}")
    if service.city_code.startswith("97"):
        department = service.city_code[:3]
    else:
        department = service.city_code[:2]
    if not department:
        department = service.structure.department
    return department


def fix_departmental_diffusion_zone_details(apps):
    services_to_update = []

    Service = apps.get_model("services", "Service")

    departmental_services = Service.objects.filter(
        diffusion_zone_type=AdminDivisionType.DEPARTMENT
    )

    problematic_services = departmental_services.filter(
        ~Q(diffusion_zone_details__length=2)
        & ~Q(diffusion_zone_details__length=3, diffusion_zone_details__startswith="97")
    )

    for service in problematic_services:
        department = get_department_for_service(service)

        service.diffusion_zone_details = department
        services_to_update.append(service)

    return services_to_update


def fix_regional_diffusion_zone_details(apps):
    services_to_update = []
    Service = apps.get_model("services", "Service")
    Department = apps.get_model("admin_express", "Department")

    regional_services = Service.objects.filter(
        diffusion_zone_type=AdminDivisionType.REGION
    )
    problematic_services = regional_services.filter(
        ~Q(diffusion_zone_details__length=2)
    )
    for service in problematic_services:
        department = get_department_for_service(service)
        try:
            region = Department.objects.get(code=department).region
        except Department.DoesNotExist:
            logger.error(f"Le département {department} n'existe pas")
            raise Department.DoesNotExist
        service.diffusion_zone_details = region
        services_to_update.append(service)

    return services_to_update


def fix_epci_diffusion_zone_details(apps):
    services_to_update = []
    Service = apps.get_model("services", "Service")
    EPCI = apps.get_model("admin_express", "EPCI")

    epci_services = Service.objects.filter(diffusion_zone_type=AdminDivisionType.EPCI)

    problematic_services = epci_services.filter(~Q(diffusion_zone_details__length=9))

    for service in problematic_services:
        department = get_department_for_service(service)

        epci = EPCI.objects.filter(departments__contains=[department]).first()

        if not epci:
            logger.error(f"L'EPCI pour le département {department} n'existe pas")
            raise EPCI.DoesNotExist

        service.diffusion_zone_details = epci.code
        services_to_update.append(service)

    return services_to_update


def fix_all_services_with_incorrect_diffusion_zone_details(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    User = apps.get_model("users", "User")

    try:
        with schema_editor.connection.cursor() as cursor:
            cursor.execute("BEGIN")

            departmental_services = fix_departmental_diffusion_zone_details(
                apps,
            )
            regional_services = fix_regional_diffusion_zone_details(
                apps,
            )
            epci_services = fix_epci_diffusion_zone_details(
                apps,
            )

            all_services = departmental_services + regional_services + epci_services

            bot_user = User.objects.get(email=settings.DORA_BOT_USER)

            for service in all_services:
                service.modification_date = timezone.now()
                service.last_editor = bot_user

            Service.objects.bulk_update(
                all_services,
                ["diffusion_zone_details", "modification_date", "last_editor"],
            )
            cursor.execute("COMMIT")
    except Exception as e:
        logger.error(
            "Erreur de transaction",
            str(e),
        )
        cursor.execute("ROLLBACK")
        raise e


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0124_rename_concerned_public_service_publics"),
    ]

    operations = [
        migrations.RunPython(
            fix_all_services_with_incorrect_diffusion_zone_details,
            migrations.RunPython.noop,
        )
    ]
