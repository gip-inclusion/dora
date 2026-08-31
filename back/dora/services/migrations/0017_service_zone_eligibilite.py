"""Add Service zone_eligibilite DI v1 field from diffusion zone.

Columns are created empty; run backfill_di_v1 --services --wet-run after deploy.
"""

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0016_service_description"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="zone_eligibilite",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=None,
                null=True,
                verbose_name="Zone d’éligibilité",
            ),
        ),
    ]
