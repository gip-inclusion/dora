import django
from django.db import migrations, models
from django.db.models import Q


def transform_national_eligibility_zones(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    Service._base_manager.filter(
        Q(zone_eligibilite__contains=["france"]) | Q(zone_eligibilite__isnull=True)
    ).update(zone_eligibilite=[])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0025_recompute_sync_checksums_model_editable_fields"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="zone_eligibilite",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=list,
                null=True,
                verbose_name="Zone d’éligibilité",
            ),
        ),
        migrations.RunPython(
            transform_national_eligibility_zones, migrations.RunPython.noop
        ),
    ]
