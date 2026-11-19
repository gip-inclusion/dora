"""
Un service ne devrait pas avoir un lien mobilisation si le formulaire Dora est activé comme mode d'orientation.
On compare mobilisation_link avec les valeurs dans les 4 champs définis dans LINK_FIELDS_BY_PRIORITY.
Seul le premier lien renseigné, par ordre de priorité, décide : les suivants ne sont jamais comparés.
S'il est identique, le lien de mobilisation est une copie de ce champ et le formulaire Dora prime.
S'il diffère — ou si aucun champ n'est renseigné — c'est une saisie personnalisée, qui est conservée.

Vu que cette migration touche à deux champs dans `SYNC_FIELDS`, il faut recalculer les checksums
des modèles nettoyés : sans ça, leur premier enregistrement, même sans modification, ferait
apparaître leurs copies encore synchronisées comme « modèle modifié ». Le calcul est figé ici
comme en 0026, à l'identique : ce qui compte est l'égalité stricte avec ce que l'application
calculera au prochain enregistrement. La formule n'est pas modifiée, et 0026 reste la migration
de référence pour les modèles que celle-ci ne touche pas.
"""

import hashlib
from collections import defaultdict

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


def clear_mobilisation_links(Service):
    """Nettoie les liens recopiés.

    Renvoie les identifiants des modèles nettoyés, et ceux des copies nettoyées
    regroupées par modèle.
    """

    qs = (
        Service._base_manager.filter(
            mobilisation_link__isnull=False,
            coach_orientation_modes__value=DORA_FORM,
        )
        .exclude(mobilisation_link="")
        .iterator(chunk_size=BATCH)
    )

    services_to_update = []
    model_ids = []
    cleared_copies_by_model = defaultdict(list)
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
            if service.is_model:
                model_ids.append(service.pk)
            elif service.model_id:
                cleared_copies_by_model[service.model_id].append(service.pk)
            break

    Service._base_manager.bulk_update(
        services_to_update,
        ["mobilisation_link", "mobilisation_modes"],
        batch_size=BATCH,
    )

    return model_ids, cleared_copies_by_model


def realign_sync_checksums(Service, model_ids, cleared_copies_by_model):
    """Réaligne les empreintes des modèles nettoyés, et celles de leurs copies."""

    models = (
        Service._base_manager.filter(pk__in=model_ids)
        .prefetch_related(*SYNC_M2M_FIELDS)
        .iterator(chunk_size=BATCH)
    )

    updated = []
    for model in models:
        previous = model.sync_checksum
        model.sync_checksum = sync_checksum(model)
        if model.sync_checksum == previous:
            continue

        # Seules les copies nettoyées de la même façon que leur modèle restent à
        # jour. Les champs comparés (`appointment_link`, etc.) n'appartiennent pas à
        # `SYNC_FIELDS` : une copie peut donc garder son lien là où son modèle perd
        # le sien. Elle diverge alors réellement, et doit afficher « modèle modifié »
        # pour pouvoir reprendre le changement.
        cleared_copy_ids = cleared_copies_by_model.get(model.pk)
        if cleared_copy_ids:
            Service._base_manager.filter(
                model_id=model.pk,
                last_sync_checksum=previous,
                pk__in=cleared_copy_ids,
            ).update(last_sync_checksum=model.sync_checksum)

        updated.append(model)
        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["sync_checksum"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["sync_checksum"])


def recompute_mobilisation_link(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    # Une seule opération : le réalignement des empreintes doit savoir quels services
    # ont été nettoyés, information que seul le nettoyage connaît. Les empreintes sont
    # calculées ensuite, sur les nouvelles valeurs.
    model_ids, cleared_copies_by_model = clear_mobilisation_links(Service)
    realign_sync_checksums(Service, model_ids, cleared_copies_by_model)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0026_recompute_sync_checksums_with_suspension_date"),
    ]

    operations = [
        migrations.RunPython(recompute_mobilisation_link, migrations.RunPython.noop),
    ]
