"""Une seule description par structure.

`full_desc` est renommée `description`, le résumé y est fusionné quand il apporte quelque
chose, puis `short_desc` et `opening_hours_details` sont supprimées.

La composition réutilise celle des services (`dora.services.descriptions`, fonctions pures
et couvertes par leurs propres tests) : le résumé est repris en tête de la description, ou
abandonné quand il ne fait que la redire.

`short_desc` et `opening_hours_details` sont conservées : plus rien ne les lit, mais elles
permettent de reprendre la fusion si besoin. Leur suppression fait l'objet d'une migration
dédiée.
"""

from django.db import migrations, models

from dora.services.descriptions import build_idf, derive_description

BATCH = 500


def merge_short_desc(apps, schema_editor):
    Structure = apps.get_model("structures", "Structure")

    weight = build_idf(
        Structure.objects.exclude(description="")
        .values_list("description", flat=True)
        .iterator(chunk_size=BATCH)
    )

    updated = []
    structures = (
        Structure.objects.exclude(short_desc="")
        .only("pk", "short_desc", "description")
        .order_by("pk")
        .iterator(chunk_size=BATCH)
    )
    for structure in structures:
        description, _ = derive_description(
            structure.short_desc, structure.description, weight
        )
        if description == structure.description:
            continue

        structure.description = description
        updated.append(structure)
        if len(updated) >= BATCH:
            Structure.objects.bulk_update(updated, ["description"])
            updated = []

    if updated:
        Structure.objects.bulk_update(updated, ["description"])


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0005_structure_name_max_length"),
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
        migrations.RunPython(
            merge_short_desc, migrations.RunPython.noop, elidable=True
        ),
    ]
