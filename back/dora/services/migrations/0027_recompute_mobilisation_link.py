"""
Un service ne devrait pas avoir un lien mobilisation si le formulaire Dora est activé comme mode d'orientation.
On compare mobilisation_link avec les valeurs dans les 4 champs définis dans LINK_FIELDS_BY_PRIORITY.
Seul le premier lien renseigné, par ordre de priorité, décide : les suivants ne sont jamais comparés.
S'il est identique, le lien de mobilisation est une copie de ce champ et le formulaire Dora prime.
S'il diffère — ou si aucun champ n'est renseigné — c'est une saisie personnalisée, qui est conservée.

Vu que cette migration touche à deux champs dans `SYNC_FIELDS`, il faut recalculer lec checksums
"""

import hashlib

from django.db import migrations

DORA_FORM = "formulaire-dora"
MOBILISATION_LINK_MODE = "utiliser-lien-mobilisation"

LINK_FIELDS_BY_PRIORITY = [
    "appointment_link",
    "online_form",
    "coach_orientation_modes_external_form_link",
    "beneficiaries_access_modes_external_form_link",
]

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
    "suspension_date",
]

SYNC_FK_FIELDS = {"fee_condition"}

SYNC_M2M_FIELDS = [
    "funding_labels",
    "categories",
    "subcategories",
    "coach_orientation_modes",
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


def clear_mobilisation_links(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    qs = (
        Service._base_manager.filter(
            mobilisation_link__isnull=False,
            coach_orientation_modes__value=DORA_FORM,
        )
        .exclude(mobilisation_link="")
        .iterator(chunk_size=BATCH)
    )

    services_to_update = []
    for service in qs:
        service_dict = service.__dict__

        for field in LINK_FIELDS_BY_PRIORITY:
            link = service_dict.get(field)

            if not link:
                continue

            if link != service_dict["mobilisation_link"]:
                break

            service.mobilisation_link = None
            # Pendant de `_validate_dora_form` : sans lien, data·inclusion rejette
            # le mode. Les deux champs doivent donc être nettoyés ensemble.
            service.mobilisation_modes = [
                mode
                for mode in (service.mobilisation_modes or [])
                if mode != MOBILISATION_LINK_MODE
            ]
            services_to_update.append(service)
            break

    Service._base_manager.bulk_update(
        services_to_update,
        ["mobilisation_link", "mobilisation_modes"],
        batch_size=BATCH,
    )


def recompute_sync_checksums(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    models = (
        Service._base_manager.filter(is_model=True)
        .prefetch_related(*SYNC_M2M_FIELDS)
        .iterator(chunk_size=BATCH)
    )

    updated = []
    for model in models:
        previous = model.sync_checksum
        model.sync_checksum = sync_checksum(model)
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
        ("services", "0026_recompute_sync_checksums_with_suspension_date"),
    ]

    operations = [
        migrations.RunPython(clear_mobilisation_links, migrations.RunPython.noop),
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
