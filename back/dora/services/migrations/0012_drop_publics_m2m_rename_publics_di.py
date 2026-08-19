"""Phase de contraction : suppression de la M2M historique `publics` et du modèle `Public`,
puis renommage de la colonne `publics_di` en `publics`.

L'écriture ayant déjà basculé sur les colonnes DI (cf. `feat/migrate-publics-write-flip`),
la M2M `publics` n'est plus alimentée : sa table de liaison peut disparaître sans perte utile.
Le renommage préserve les données de `publics_di` (Django émet un simple `ALTER TABLE ... RENAME COLUMN`).

Ordre des opérations : on retire d'abord la M2M pour libérer le nom `publics`, on renomme
ensuite `publics_di` -> `publics`, et on supprime enfin le modèle `Public` désormais sans référence.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models

import dora.services.models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0011_service_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="publics",
        ),
        migrations.RenameField(
            model_name="service",
            old_name="publics_di",
            new_name="publics",
        ),
        migrations.AlterField(
            model_name="service",
            name="publics",
            field=ArrayField(
                models.CharField(
                    max_length=255,
                    validators=[dora.services.models.validate_corresponding_di_publics],
                ),
                blank=True,
                default=list,
                verbose_name="Publics (référentiel DI)",
            ),
        ),
        migrations.DeleteModel(
            name="Public",
        ),
    ]
