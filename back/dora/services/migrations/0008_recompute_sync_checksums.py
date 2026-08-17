"""Recalcule les empreintes de synchronisation après le passage de `kinds` à `kind`.

`kind` entre dans `SYNC_FIELDS` et `kinds` sort de `SYNC_M2M_FIELDS` : l'empreinte d'un modèle
change donc de valeur. Sans ce recalcul, les ~3 000 modèles et toutes leurs copies encore
synchronisées apparaîtraient d'un coup comme « modèle modifié » aux utilisateurs.

`update_sync_checksum` est volontairement importée du code applicatif plutôt que recopiée ici :
ce qui compte est l'égalité stricte avec ce que l'application calculera au prochain
enregistrement — une copie figée qui divergerait produirait exactement le faux « modèle
modifié » que cette migration cherche à éviter. Cette égalité suppose que la fonction ne hache
que des valeurs identiques sur un modèle historique et sur le vrai modèle : c'est pourquoi
elle hache l'identifiant des clés étrangères et non l'instance liée, dont le `repr()` dépend
du `__str__` absent ici.

Elle suppose `Service.kind` déjà renseigné : la colonne est remplie par la commande
`backfill_service_kind` du déploiement précédent, lancée en one-off avant celui-ci.
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

        # Seules les copies qui étaient à jour le restent : celles dont l'empreinte diffère
        # déjà ont de vraies modifications en attente, à ne pas masquer.
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
        ("services", "0007_service_kind"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
