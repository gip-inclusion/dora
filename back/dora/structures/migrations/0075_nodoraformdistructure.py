# Generated by Django 4.2.20 on 2025-03-28 12:13

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0074_alter_structure_code_safir_pe_alter_structure_siret"),
    ]

    operations = [
        migrations.CreateModel(
            name="DisabledDoraFormDIStructure",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("source", models.CharField(max_length=255, verbose_name="Source")),
                (
                    "structure_id",
                    models.CharField(
                        max_length=1024, verbose_name="ID de la structure"
                    ),
                ),
                ("comment", models.TextField(blank=True, verbose_name="Commentaire")),
            ],
            options={
                "verbose_name": "structure DI avec formulaire Dora désactivé",
                "verbose_name_plural": "structures DI avec formulaire Dora désactivé",
            },
        ),
    ]
