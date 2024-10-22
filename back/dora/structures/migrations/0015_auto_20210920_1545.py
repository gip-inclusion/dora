# Generated by Django 3.2.5 on 2021-09-20 13:45

from django.db import migrations, models

import dora.structures.models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0014_structure_department"),
    ]

    operations = [
        migrations.AlterField(
            model_name="structure",
            name="code_safir_pe",
            field=models.CharField(
                blank=True,
                db_index=True,
                max_length=5,
                null=True,
                unique=True,
                validators=[dora.structures.models.validate_safir],
                verbose_name="Code Safir Pole Emploi",
            ),
        ),
        migrations.AlterField(
            model_name="structure",
            name="source",
            field=models.CharField(
                blank=True,
                choices=[
                    ("DORA", "Équipe DORA"),
                    ("ITOU", "Import ITOU"),
                    ("PORTEUR", "Porteur"),
                    ("PE", "API Référentiel Agence PE"),
                ],
                db_index=True,
                max_length=12,
            ),
        ),
    ]