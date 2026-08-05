import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_protect_structure_fks"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="modes_mobilisation",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("envoyer-un-courriel", "Envoyer un courriel"),
                        ("se-presenter", "Se présenter"),
                        ("telephoner", "Téléphoner"),
                        (
                            "utiliser-lien-mobilisation",
                            "Utiliser le lien de mobilisation",
                        ),
                        ("formulaire-dora", "Via le formulaire DORA"),
                    ],
                    max_length=30,
                ),
                blank=True,
                default=list,
                size=None,
                verbose_name="Comment mobiliser le service",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="mobilisable_par",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("usagers", "Usagers"),
                        ("professionnels", "Professionnels"),
                    ],
                    max_length=20,
                ),
                blank=True,
                default=list,
                size=None,
                verbose_name="Qui peut mobiliser le service",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="mobilisation_precisions",
            field=models.TextField(
                blank=True,
                verbose_name="Précisions sur les modalités de mobilisation",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="lien_mobilisation",
            field=models.URLField(
                blank=True, max_length=280, verbose_name="Lien de mobilisation"
            ),
        ),
    ]
