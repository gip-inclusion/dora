"""Recalcule les empreintes de synchronisation après la bascule d'écriture
des champs de mobilisation.

`mobilisation_*` remplace les 8 champs coach/bénéficiaire dans `SYNC_FIELDS` /
`SYNC_M2M_FIELDS`. Sans ce recalcul, les modèles et leurs copies encore
synchronisées apparaîtraient d'un coup comme « modèle modifié ».
"""

from django.db import migrations

from dora.services.utils import (
    SYNC_CUSTOM_M2M_FIELDS,
    SYNC_M2M_FIELDS,
    update_sync_checksum,
)

BATCH = 500


def recompute_sync_checksums(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    updated = []
    models = (
        Service._base_manager.filter(is_model=True)
        .prefetch_related(*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS)
        .iterator(chunk_size=BATCH)
    )
    for model in models:
        previous = model.sync_checksum
        model.sync_checksum = update_sync_checksum(model)
        if model.sync_checksum == previous:
            continue

        Service._base_manager.filter(
            model_id=model.pk, last_sync_checksum=previous
        ).update(last_sync_checksum=model.sync_checksum)

        updated.append(model)
        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["sync_checksum"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["sync_checksum"])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0014_mobilisation_fields"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
