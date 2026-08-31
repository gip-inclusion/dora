"""Add Structure.reseaux_porteurs for di_v1 from typology and national_labels.

Column is created empty; run backfill_di_v1 --wet-run after deploy.
"""

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0003_protect_structure_fks"),
    ]

    operations = [
        migrations.AddField(
            model_name="structure",
            name="reseaux_porteurs",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=None,
                null=True,
                verbose_name="Réseaux porteurs",
            ),
        ),
    ]
