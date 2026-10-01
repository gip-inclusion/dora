"""Recalcule les empreintes de synchronisation après la révision des champs synchronisés.

`SYNC_FIELDS` ne retient plus que les champs qu'un modèle expose à l'édition (cf. le
formulaire `ModelEditionForm`) : les champs hérités de la v1 en sortent, les champs
`description`, `conditions_acces`, `mobilisation_*` et `mobilisable_by` y entrent, et
`funding_labels` rejoint les champs Many to many. L'empreinte d'un modèle change donc de
valeur. Sans ce recalcul, le premier enregistrement d'un modèle, même sans modification,
ferait apparaître toutes ses copies encore synchronisées comme « modèle modifié ».

Comme en 0008, 0010 et 0021, le calcul est figé ici plutôt qu'importé de
`dora.services.utils` : ce qui compte est l'égalité stricte avec ce que l'application
calculera au prochain enregistrement, mais cette égalité est la charge de la migration de
recalcul la plus récente, pas de celle-ci. La copie reproduit donc le code applicatif tel
qu'il est au moment du déploiement. La réduction des membres d'énumération à leur valeur n'y
figure pas : les valeurs relues en base sont toujours des chaînes nues.

L'ordre des champs, et notamment celui des champs Many to many, fait partie de la formule :
il doit suivre celui de `dora.services.utils` à l'identique.
"""

import hashlib

from django.db import migrations

SYNC_FIELDS = [
    "name",
    "description",
    "kind",
    "publics",
    "publics_precisions",
    "conditions_acces",
    "forms",
    "fee_condition",
    "fee_details",
    "mobilisable_by",
    "mobilisation_modes",
    "mobilisation_details",
    "mobilisation_link",
    "duration_weekly_hours",
    "duration_weeks",
    "update_frequency",
]

SYNC_FK_FIELDS = {"fee_condition"}

SYNC_M2M_FIELDS = [
    "funding_labels",
    "categories",
    "subcategories",
]

BATCH = 500


def sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        attr = f"{field}_id" if field in SYNC_FK_FIELDS else field
        md5.update(repr(getattr(service, attr)).encode())
    for m2m_field in SYNC_M2M_FIELDS:
        pks = sorted(obj.pk for obj in getattr(service, m2m_field).all())
        md5.update(repr(pks).encode())

    return md5.hexdigest()


def recompute_sync_checksums(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    updated = []
    models = (
        Service._base_manager.filter(is_model=True)
        .prefetch_related(*SYNC_M2M_FIELDS)
        .iterator(chunk_size=BATCH)
    )
    for model in models:
        previous = model.sync_checksum
        model.sync_checksum = sync_checksum(model)
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
        ("services", "0024_alter_service_name"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
