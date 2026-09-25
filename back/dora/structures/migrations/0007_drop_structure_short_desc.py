"""Supprime les colonnes `short_desc` et `opening_hours_details`.

La migration 0006 a fusionné les résumés dans `description` ; ces deux champs n'étaient
conservés que pour pouvoir reprendre cette fusion.

Migration destructive : à passer dans un déploiement dédié, une fois la 0006 vérifiée.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0006_structure_description"),
    ]

    operations = [
        migrations.RemoveField(model_name="structure", name="short_desc"),
        migrations.RemoveField(model_name="structure", name="opening_hours_details"),
    ]
