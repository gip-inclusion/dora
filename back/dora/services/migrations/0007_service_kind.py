"""Ajoute `Service.kind`, dérivé de la M2M historique `Service.kinds`.

La colonne est créée vide : le remplissage de l'existant est confié à la commande
`backfill_service_kind` (à lancer avec `--wet-run` juste après le déploiement), qui porte
aussi la règle de réduction `dora.services.utils.compute_service_kind`. Les services sans
type gardent un `kind` à `NULL`.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0006_service_publics_di_service_publics_precisions"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("accompagnement", "Accompagnement"),
                    ("aide-financiere", "Aide financière"),
                    ("aide-materielle", "Aide materielle"),
                    ("atelier", "Atelier"),
                    ("formation", "Formation"),
                    ("information", "Information"),
                ],
                default=None,
                max_length=255,
                null=True,
                verbose_name="Type de service",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="kinds",
            field=models.ManyToManyField(
                blank=True,
                to="services.servicekind",
                verbose_name="Types de service (déprécié)",
            ),
        ),
    ]
