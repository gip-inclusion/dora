"""Recalcule les empreintes de synchronisation après le passage de `kinds` à `kind`.

`kind` entre dans les champs synchronisés et `kinds` en sort : l'empreinte d'un modèle change
donc de valeur. Sans ce recalcul, les ~3 000 modèles et toutes leurs copies encore
synchronisées apparaîtraient d'un coup comme « modèle modifié » aux utilisateurs.

Le calcul est figé ici plutôt qu'importé de `dora.services.utils` : celle-ci suit le schéma
courant et référence des colonnes qui n'existent pas encore à ce point de l'historique —
`full_desc` n'est renommé en `description` que par `0011_service_description`, et un rejeu de
cette migration sur une base peuplée échouerait. Ce qui compte est l'égalité stricte avec ce
que l'application calculera au prochain enregistrement, mais cette égalité est la charge de la
migration de recalcul la plus récente, pas de celle-ci : à l'époque de cette migration, seul
l'état de l'époque est correct. La copie reproduit donc le code applicatif tel qu'il était au
moment du déploiement, y compris le hachage des clés étrangères par leur identifiant plutôt
que par l'instance liée, dont le `repr()` dépend d'un `__str__` absent des modèles historiques.

Elle suppose `Service.kind` déjà renseigné : la colonne est remplie par la commande
`backfill_service_kind` du déploiement précédent, lancée en one-off avant celui-ci.
"""

import hashlib

from django.db import migrations

SYNC_FIELDS = [
    "name",
    "short_desc",
    "full_desc",
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
    "publics",
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
        ("services", "0007_service_kind"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
