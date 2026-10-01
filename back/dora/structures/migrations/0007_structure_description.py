"""Une seule description par structure.

`full_desc` est renommée `description`. Le résumé y est fusionné après déploiement par la
commande `backfill_structure_descriptions`, pour que la migration ne dépende pas du code
applicatif.

`short_desc` et `opening_hours_details` sont conservées : plus rien ne les lit, mais elles
permettent de reprendre la fusion si besoin. Leur suppression fait l'objet d'une migration
dédiée.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0006_structure_name_max_length"),
    ]

    operations = [
        migrations.RenameField(
            model_name="structure", old_name="full_desc", new_name="description"
        ),
        migrations.AlterField(
            model_name="structure",
            name="description",
            field=models.TextField(blank=True, verbose_name="Description"),
        ),
    ]
