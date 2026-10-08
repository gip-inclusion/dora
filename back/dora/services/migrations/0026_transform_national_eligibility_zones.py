from django.db import migrations

BATCH = 500


def transform_national_eligibility_zones(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    Service._base_manager.filter(zone_eligibilite__contains=["france"]).update(
        zone_eligibilite=[]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0025_recompute_sync_checksums_model_editable_fields"),
    ]

    operations = [
        migrations.RunPython(
            transform_national_eligibility_zones, migrations.RunPython.noop
        ),
    ]
