"""Limite Structure.name à 150 caractères, côté Django uniquement.

La colonne reste un varchar(255) : les quelques noms plus longs déjà en base
restent lisibles, et le déploiement n'a pas d'ALTER TABLE à passer.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0004_structure_reseaux_porteurs"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            state_operations=[
                migrations.AlterField(
                    model_name="structure",
                    name="name",
                    field=models.CharField(
                        db_index=True, max_length=150, verbose_name="Nom"
                    ),
                ),
            ],
            database_operations=[],
        ),
    ]
