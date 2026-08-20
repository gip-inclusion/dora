"""Recalcule les empreintes de synchronisation après la bascule d'écriture des publics.

Les colonnes DI (`publics_di` / `publics_precisions`) remplacent la M2M `publics` dans le
formulaire : la composition de l'empreinte change donc, et sans ce recalcul les modèles et
toutes leurs copies encore synchronisées apparaîtraient d'un coup comme « modèle modifié ».

Comme en 0008, le calcul est figé ici plutôt qu'importé de `dora.services.utils` : celle-ci
suit le schéma courant et référence des colonnes qui n'existent pas encore à ce point de
l'historique. Ce qui compte est l'égalité stricte avec ce que l'application calculera au
prochain enregistrement, mais cette égalité est la charge de la migration de recalcul la plus
récente, pas de celle-ci : à l'époque de cette migration, seul l'état de l'époque est correct.
La copie reproduit donc le code applicatif tel qu'il était au moment du déploiement — y
compris l'ordre de référence des publics DI, figé lui aussi pour qu'une évolution du
référentiel `data-inclusion` ne change pas rétroactivement la normalisation.
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

DI_PUBLICS_ORDER = {
    public: index
    for index, public in enumerate(
        [
            "tous-publics",
            "actifs",
            "beneficiaires-des-minimas-sociaux",
            "demandeurs-emploi",
            "etudiants",
            "familles",
            "femmes",
            "jeunes",
            "personnes-en-situation-de-handicap",
            "personnes-en-situation-durgence",
            "personnes-en-situation-juridique-specifique",
            "personnes-exilees",
            "residents-qpv-frr",
            "seniors",
        ]
    )
}

BATCH = 500


def normalize_publics_di(publics):
    return sorted(set(publics), key=DI_PUBLICS_ORDER.__getitem__)


def sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        attr = f"{field}_id" if field in SYNC_FK_FIELDS else field
        md5.update(repr(getattr(service, attr)).encode())
    for m2m_field in [*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS]:
        pks = sorted(obj.pk for obj in getattr(service, m2m_field).all())
        md5.update(repr(pks).encode())

    return md5.hexdigest()


def normalize_publics(Service):
    # L'empreinte hache `publics_di` tel quel : la normalisation doit être faite en base
    # avant le recalcul, sinon les lignes historiques garderaient leur ordre de saisie et
    # repasseraient en « modèle modifié » à la première écriture qui les normalise.
    updated = []
    services = Service._base_manager.exclude(publics_di=[]).iterator(chunk_size=BATCH)
    for service in services:
        normalized = normalize_publics_di(service.publics_di)
        if normalized == service.publics_di:
            continue

        service.publics_di = normalized
        updated.append(service)
        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["publics_di"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["publics_di"])


def recompute_sync_checksums(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    normalize_publics(Service)

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
        ("services", "0009_remove_service_kinds"),
    ]

    operations = [
        migrations.RunPython(recompute_sync_checksums, migrations.RunPython.noop),
    ]
