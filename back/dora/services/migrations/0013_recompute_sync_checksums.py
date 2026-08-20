"""Recalcule les empreintes de synchronisation après la sortie de `short_desc`.

L'empreinte hache la valeur de chacun des champs synchronisés : en retirer un change
l'empreinte de tous les modèles. Sans ce recalcul, les ~2 800 modèles et toutes leurs copies
encore synchronisées apparaîtraient d'un coup comme « modèle modifié » aux utilisateurs.

Même patron que `0008_recompute_sync_checksums`, dont le préambule détaille pourquoi le calcul
est figé ici plutôt qu'importé du code applicatif. Ce qui compte est l'égalité stricte avec ce
que l'application calculera au prochain enregistrement — une copie qui divergerait produirait
exactement le faux « modèle modifié » que cette migration cherche à éviter. Cette migration
étant la plus récente à recalculer les empreintes, c'est elle qui porte cette égalité :
`test_migrations_sync_checksum.py` la vérifie, et rougira au prochain changement des champs
synchronisés — signe qu'une nouvelle migration de recalcul est nécessaire.
"""

import hashlib

from django.db import migrations

SYNC_FIELDS = [
    "name",
    "description",
    "is_cumulative",
    "fee_condition",
    "fee_details",
    "beneficiaries_access_modes_external_form_link",
    "beneficiaries_access_modes_external_form_link_text",
    "beneficiaries_access_modes_other",
    "coach_orientation_modes_external_form_link",
    "coach_orientation_modes_external_form_link_text",
    "coach_orientation_modes_other",
    "duration_weekly_hours",
    "duration_weeks",
    "forms",
    "kind",
    "online_form",
    "publics_di",
    "publics_precisions",
    "qpv_or_zrr",
    "recurrence",
    "suspension_date",
]

SYNC_FK_FIELDS = {"fee_condition"}

SYNC_M2M_FIELDS = [
    "categories",
    "subcategories",
    "beneficiaries_access_modes",
    "coach_orientation_modes",
]

SYNC_CUSTOM_M2M_FIELDS = [
    "access_conditions",
    "requirements",
    "credentials",
]

BATCH = 500


def sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        attr = f"{field}_id" if field in SYNC_FK_FIELDS else field
        md5.update(repr(getattr(service, attr)).encode())
    for m2m_field in [*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS]:
        pks = sorted(obj.pk for obj in getattr(service, m2m_field).all())
        md5.update(repr(pks).encode())

    return md5.hexdigest()


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
        ("services", "0012_remove_service_short_desc"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
