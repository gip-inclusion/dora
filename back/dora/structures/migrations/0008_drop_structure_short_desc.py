"""Supprime les colonnes `short_desc` et `opening_hours_details`.

La commande `backfill_structure_descriptions` a fusionné les résumés dans `description` ;
ces deux champs n'étaient conservés que pour pouvoir reprendre cette fusion. La commande,
qui lit `short_desc`, est supprimée avec eux.

Migration destructive : à passer dans un déploiement dédié, une fois la fusion vérifiée.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0007_structure_description"),
    ]

    operations = [
        migrations.RemoveField(model_name="structure", name="short_desc"),
        migrations.RemoveField(model_name="structure", name="opening_hours_details"),
    ]
