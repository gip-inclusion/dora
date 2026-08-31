"""Add Service mobilisation DI v1 fields from orientation modes and links.

Columns are created empty; run backfill_di_v1 --services --wet-run after deploy.
"""

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0013_drop_publics_m2m_rename_publics_di"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="mobilisation_details",
            field=models.TextField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Précisions sur la mobilisation",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="mobilisation_link",
            field=models.URLField(
                blank=True,
                default=None,
                null=True,
                verbose_name="Lien de mobilisation",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="mobilisable_by",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=None,
                null=True,
                verbose_name="Mobilisable par",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="mobilisation_modes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=None,
                null=True,
                verbose_name="Modes de mobilisation",
            ),
        ),
    ]
