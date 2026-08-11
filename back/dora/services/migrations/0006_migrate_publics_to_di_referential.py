"""Ajoute `publics_di` (ArrayField) et `publics_precisions` (TextField) à Service et les remplit
à partir de la relation M2M historique `Service.publics`.

La logique de remplissage vit dans `dora.services.utils.compute_publics_di` (partagée avec le
signal de double écriture et la commande de réconciliation). `tous-publics` n'est jamais stocké :
un tableau vide signifie « tous publics » et sera réinterprété pour l'affichage.
"""

from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models

from dora.services.models import validate_corresponding_di_publics
from dora.services.utils import compute_publics_di


def backfill_publics(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    updated = []
    qs = (
        Service.objects.filter(publics__isnull=False)
        .distinct()
        .prefetch_related("publics")
        .only("pk")
        .iterator(chunk_size=500)
    )
    for service in qs:
        service.publics_di, service.publics_precisions = compute_publics_di(service)
        updated.append(service)

        if len(updated) >= 500:
            Service.objects.bulk_update(updated, ["publics_di", "publics_precisions"])
            updated = []

    if updated:
        Service.objects.bulk_update(updated, ["publics_di", "publics_precisions"])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0005_savedsearch_kinds_array"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="publics_di",
            field=ArrayField(
                models.CharField(
                    max_length=255,
                    validators=[validate_corresponding_di_publics],
                ),
                default=list,
                blank=True,
                verbose_name="Publics (référentiel DI)",
            ),
        ),
        migrations.AddField(
            model_name="service",
            name="publics_precisions",
            field=models.TextField(
                blank=True, default="", verbose_name="Précisions publics"
            ),
        ),
        migrations.RunPython(backfill_publics, migrations.RunPython.noop),
    ]
