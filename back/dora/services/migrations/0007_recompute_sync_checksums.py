"""Recalcule les checksums de synchronisation après le changement de `SYNC_FIELDS`.

Sans ce recalcul, le prochain enregistrement d'un modèle de service ferait
basculer à tort tous les services qui en découlent en « modèle modifié ».
"""

import hashlib

from django.db import migrations

# Copie figée de `dora.services.utils` telle qu'elle est au moment de cette
# migration : le calcul ne doit pas suivre les évolutions ultérieures du code
# applicatif, sous peine de produire d'autres checksums lorsque l'historique des
# migrations est rejoué. Le corollaire est qu'un prochain changement de ces
# listes devra s'accompagner de sa propre migration de recalcul — c'est ce que
# surveille `test_migration_checksum_matches_application`.
SYNC_FIELDS = [
    "name",
    "short_desc",
    "full_desc",
    "is_cumulative",
    "fee_condition",
    "fee_details",
    "modes_mobilisation",
    "mobilisable_par",
    "mobilisation_precisions",
    "lien_mobilisation",
    "duration_weekly_hours",
    "duration_weeks",
    "forms",
    "online_form",
    "qpv_or_zrr",
    "recurrence",
    "suspension_date",
]

SYNC_M2M_FIELDS = [
    "kinds",
    "categories",
    "subcategories",
    "access_conditions",
    "publics",
    "requirements",
    "credentials",
]


def compute_sync_checksum(service):
    md5 = hashlib.md5(usedforsecurity=False)
    for field in SYNC_FIELDS:
        value = getattr(service, field)
        if field == "fee_condition":
            # `repr()` d'une instance liée dépend de son `__str__`, que les
            # modèles historiques n'ont pas : on reproduit celui d'`EnumModel`.
            value_repr = "None" if value is None else f"<ServiceFee: {value.label}>"
        else:
            value_repr = repr(value)
        md5.update(value_repr.encode())

    for m2m_field in SYNC_M2M_FIELDS:
        md5.update(
            repr(
                list(
                    getattr(service, m2m_field)
                    .all()
                    .values_list("pk", flat=True)
                    .order_by("pk")
                )
            ).encode()
        )

    return md5.hexdigest()


def forward(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    # Les modèles de service vivent dans la même table, distingués par `is_model` :
    # le manager qui filtre habituellement pour nous n'existe pas ici.
    service_models = Service.objects.filter(is_model=True).select_related(
        "fee_condition"
    )
    for service_model in service_models.iterator(chunk_size=200):
        previous_checksum = service_model.sync_checksum
        checksum = compute_sync_checksum(service_model)
        if checksum == previous_checksum:
            continue

        # Les services encore synchronisés avec leur modèle doivent le rester.
        Service.objects.filter(
            is_model=False,
            model_id=service_model.id,
            last_sync_checksum=previous_checksum,
        ).update(last_sync_checksum=checksum)
        Service.objects.filter(pk=service_model.pk).update(sync_checksum=checksum)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0006_migrate_mobilisation_data"),
    ]

    operations = [
        migrations.RunPython(forward, migrations.RunPython.noop, elidable=True),
    ]
