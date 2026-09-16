"""Dédoublonne les documents par nom de fichier, avant l'entrée en vigueur du validateur.

Le dédoublonnage touche `forms`, qui entre dans l'empreinte de synchronisation : les
empreintes des modèles concernés sont donc recalculées dans la foulée. Sans ce recalcul,
l'empreinte stockée resterait celle d'avant le dédoublonnage et le prochain enregistrement
du modèle ferait apparaître d'un coup toutes ses copies comme « modèle modifié », alors que
les deux côtés ont été dédoublonnés à l'identique.

Comme en 0008 et 0010, le calcul est figé ici plutôt qu'importé de `dora.services.utils` :
celle-ci suit le schéma courant, et cette migration doit continuer de produire l'empreinte
de l'état d'aujourd'hui même après une évolution des champs synchronisés. L'égalité stricte
avec ce que l'application calculera au prochain enregistrement est la charge de la migration
de recalcul la plus récente — ce rôle passe ici de 0010 à celle-ci.
"""

import hashlib

import django.contrib.postgres.fields
from django.db import migrations, models

import dora.services.models

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
    "publics",
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


def deduplicate_form_names(Service):
    """Écarte les documents en double avant l'entrée en vigueur du validateur.

    Seul le nom de fichier est affiché à l'utilisateur : deux clés dont le nom coïncide
    sont indistinguables dans le formulaire. On conserve la première occurrence et on
    retire les suivantes de la liste (les fichiers stockés ne sont pas supprimés, ils
    peuvent être référencés ailleurs).
    """
    updated = []
    services = Service._base_manager.exclude(forms=[]).iterator(chunk_size=BATCH)
    for service in services:
        seen_names = set()
        deduplicated_forms = []
        for form in service.forms:
            name = form.rsplit("/", 1)[-1]
            if name in seen_names:
                continue
            seen_names.add(name)
            deduplicated_forms.append(form)

        if deduplicated_forms == service.forms:
            continue

        service.forms = deduplicated_forms
        updated.append(service)
        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["forms"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["forms"])


def recompute_sync_checksums(Service):
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


def deduplicate_forms(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    # L'ordre compte : l'empreinte hache `forms`, elle ne peut être recalculée qu'une fois
    # les doublons retirés.
    deduplicate_form_names(Service)
    recompute_sync_checksums(Service)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0019_service_horaires_accueil"),
    ]

    operations = [
        migrations.RunPython(deduplicate_forms, reverse_code=migrations.RunPython.noop),
        migrations.AlterField(
            model_name="service",
            name="forms",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                validators=[dora.services.models.validate_unique_form_names],
                verbose_name="Partagez les documents à compléter",
            ),
        ),
    ]
