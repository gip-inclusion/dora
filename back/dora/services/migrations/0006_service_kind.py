"""Ajoute `Service.kind` et le remplit à partir de la M2M historique `Service.kinds`.

Un service peut porter plusieurs types ; la règle de réduction vit dans
`dora.services.utils.compute_service_kind` (partagée avec le signal de double écriture et la
commande de réconciliation). Les services sans type gardent un `kind` vide.
"""

from django.db import migrations, models

from dora.services.utils import compute_service_kind

BATCH = 500


def backfill_kind(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    updated = []
    qs = (
        Service._base_manager.prefetch_related("kinds")
        .only("pk")
        .iterator(chunk_size=BATCH)
    )
    for service in qs:
        service.kind = compute_service_kind(service)
        updated.append(service)

        if len(updated) >= BATCH:
            Service._base_manager.bulk_update(updated, ["kind"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["kind"])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0005_savedsearch_kinds_array"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="kind",
            field=models.CharField(
                blank=True,
                choices=[
                    ("accompagnement", "Accompagnement"),
                    ("aide-financiere", "Aide financière"),
                    ("aide-materielle", "Aide materielle"),
                    ("atelier", "Atelier"),
                    ("formation", "Formation"),
                    ("information", "Information"),
                ],
                db_index=True,
                default="",
                max_length=255,
                verbose_name="Type de service",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="kinds",
            field=models.ManyToManyField(
                blank=True,
                to="services.servicekind",
                verbose_name="Types de service (déprécié)",
            ),
        ),
        migrations.RunPython(backfill_kind, migrations.RunPython.noop),
    ]
