from django.db import migrations
from django.db.models import Q
from django.utils import timezone

from dora.admin_express.models import AdminDivisionType


def get_department_for_service(service):
    if service.city_code.startswith("97"):
        department = service.city_code[:3]
    else:
        department = service.city_code[:2]
    if not department:
        department = service.structure.department
    return department


def fix_departmental_diffusion_zone_details(apps):
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
        service.modification_date = timezone.now()
        service.save()


def fix_regional_diffusion_zone_details(apps):
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
            continue
        service.diffusion_zone_details = region
        service.modification_date = timezone.now()
        service.save()


def fix_epci_diffusion_zone_details(apps):
    Service = apps.get_model("services", "Service")
    EPCI = apps.get_model("admin_express", "EPCI")

    epci_services = Service.objects.filter(diffusion_zone_type=AdminDivisionType.EPCI)

    problematic_services = epci_services.filter(~Q(diffusion_zone_details__length=9))

    for service in problematic_services:
        department = get_department_for_service(service)

        epci = EPCI.objects.filter(departments__contains=[department]).first()

        if not epci:
            continue

        service.diffusion_zone_details = epci.code
        service.modification_date = timezone.now()
        service.save()


def fix_all_services_with_incorrect_diffusion_zone_details(apps, schema_editor):
    fix_departmental_diffusion_zone_details(apps)
    fix_regional_diffusion_zone_details(apps)
    fix_epci_diffusion_zone_details(apps)


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
