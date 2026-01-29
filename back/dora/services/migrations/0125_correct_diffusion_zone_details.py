import logging

from django.conf import settings
from django.db import migrations
from django.db.models import Q
from django.utils import timezone

from dora.admin_express.models import AdminDivisionType
from dora.admin_express.utils import arrdt_to_main_insee_code

logger = logging.getLogger(__name__)


def get_city_by_code(apps, city_code):
    City = apps.get_model("decoupage_administratif", "City")

    insee_code = arrdt_to_main_insee_code(city_code)

    try:
        city = City.objects.get(code=insee_code)
    except City.DoesNotExist:
        logger.error(f"La ville dont le code est {city_code} n'existe pas")
        return None

    return city


def fix_departmental_diffusion_zone_details(apps):
    services_to_update = []

    Service = apps.get_model("services", "Service")

    departmental_services = Service.objects.filter(
        diffusion_zone_type=AdminDivisionType.DEPARTMENT
    )

    # Les services pour les régions doivent avoir soit deux chiffres soit
    # trois chiffres qui commencent avec `97` pour les régions DOM-TOM.
    problematic_services = departmental_services.filter(
        ~Q(diffusion_zone_details__length=2)
        & ~Q(diffusion_zone_details__length=3, diffusion_zone_details__startswith="97")
    )

    for service in problematic_services:
        city_code = (
            service.city_code if service.city_code else service.structure.city_code
        )

        if not city_code:
            logger.warning(f"Le service dont l'id {service.id} n'a pas de city_code.")
            continue

        city = get_city_by_code(apps, city_code)

        if not city:
            continue

        department = city.department

        service.diffusion_zone_details = department
        services_to_update.append(service)

        logger.info(
            f"Le service avec l'id {service.id} est du type 'département' et ses diffusion_zone_details sont {department}."
        )

    return services_to_update


def fix_regional_diffusion_zone_details(apps):
    services_to_update = []
    Service = apps.get_model("services", "Service")

    regional_services = Service.objects.filter(
        diffusion_zone_type=AdminDivisionType.REGION
    )
    problematic_services = regional_services.filter(
        ~Q(diffusion_zone_details__length=2)
    )
    for service in problematic_services:
        city = get_city_by_code(apps, service.city_code)

        if not city:
            continue

        region = city.region
        service.diffusion_zone_details = region
        services_to_update.append(service)

        logger.info(
            f"Le service avec l'id {service.id} est du type 'région' et ses diffusion_zone_details sont {region}."
        )

    return services_to_update


def fix_epci_diffusion_zone_details(apps):
    services_to_update = []
    Service = apps.get_model("services", "Service")

    epci_services = Service.objects.filter(diffusion_zone_type=AdminDivisionType.EPCI)

    problematic_services = epci_services.filter(~Q(diffusion_zone_details__length=9))

    for service in problematic_services:
        city = get_city_by_code(apps, service.city_code)

        if not city:
            continue

        epci_code = city.epci
        service.diffusion_zone_details = epci_code
        services_to_update.append(service)

        logger.info(
            f"Le service avec l'id {service.id} est du type 'epci' et ses diffusion_zone_details sont {epci_code}."
        )

    return services_to_update


def fix_all_services_with_incorrect_diffusion_zone_details(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    User = apps.get_model("users", "User")

    try:
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
    except Exception as e:
        logger.error(
            "Erreur de transaction pour le profil %d : %s",
            str(e),
        )
        raise e


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0124_b_rename_publics_m2m_table_django6"),
    ]

    operations = [
        migrations.RunPython(
            fix_all_services_with_incorrect_diffusion_zone_details,
            migrations.RunPython.noop,
        )
    ]
