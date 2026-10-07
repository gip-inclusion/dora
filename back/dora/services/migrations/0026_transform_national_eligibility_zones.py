from django.db import migrations

BATCH = 500


def transform_national_eligiblity_zones(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    national_services = Service._base_manager.filter(
        zone_eligibilite__contains=["france"]
    ).iterator(chunk_size=BATCH)
    updated_services = []

    for national_service in national_services:
        national_service.zone_eligibilite = []
        updated_services.append(national_service)

        if len(updated_services) >= BATCH:
            Service._base_manager.bulk_update(updated_services, ["zone_eligibilite"])
            updated_services = []

    if updated_services:
        Service._base_manager.bulk_update(updated_services, ["zone_eligibilite"])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0025_recompute_sync_checksums_model_editable_fields"),
    ]

    operations = [
        migrations.RunPython(
            transform_national_eligiblity_zones, migrations.RunPython.noop
        ),
    ]
