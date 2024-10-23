import django.contrib.postgres.indexes
from django.contrib.postgres.operations import TrigramExtension
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        TrigramExtension(),
        migrations.CreateModel(
            name="Establishment",
            fields=[
                (
                    "siret",
                    models.CharField(
                        max_length=14,
                        primary_key=True,
                        serialize=False,
                        verbose_name="Siret",
                    ),
                ),
                ("siren", models.CharField(max_length=9, verbose_name="Siren")),
                ("denomination", models.CharField(max_length=100, verbose_name="Nom")),
                ("ape", models.CharField(max_length=6)),
                ("code_cedex", models.CharField(max_length=9)),
                ("code_commune", models.CharField(max_length=5)),
                ("code_postal", models.CharField(max_length=5)),
                ("complement_adresse", models.CharField(max_length=38)),
                ("distribution_speciale", models.CharField(max_length=26)),
                ("enseigne1", models.CharField(max_length=50)),
                ("enseigne2", models.CharField(max_length=50)),
                ("enseigne3", models.CharField(max_length=50)),
                ("is_siege", models.BooleanField()),
                ("repetition_index", models.CharField(max_length=1)),
                ("libelle_cedex", models.CharField(max_length=100)),
                ("libelle_commune", models.CharField(max_length=100)),
                ("libelle_voie", models.CharField(max_length=100)),
                ("nic", models.CharField(max_length=5)),
                ("numero_voie", models.CharField(max_length=4)),
                ("diffusable", models.BooleanField()),
                ("type_voie", models.CharField(max_length=4)),
                ("denomination_parent", models.TextField(blank=True, default="")),
                (
                    "sigle_parent",
                    models.CharField(blank=True, default="", max_length=20),
                ),
                ("longitude", models.FloatField(blank=True, null=True)),
                ("latitude", models.FloatField(blank=True, null=True)),
                ("full_search_text", models.TextField()),
            ],
        ),
        migrations.AddIndex(
            model_name="establishment",
            index=django.contrib.postgres.indexes.GinIndex(
                fields=["full_search_text"],
                name="full_text_trgm_idx",
                opclasses=("gin_trgm_ops",),
            ),
        ),
    ]
