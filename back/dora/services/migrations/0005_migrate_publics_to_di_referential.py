"""Migration adds `publics_di` (ArrayField) and `publics_precisions` (TextField) to Service and
backfills them from the existing `Service.publics` M2M.

Services with an empty publics M2M fall back to an LLM suggestion loaded from an
optional JSON artifact under migrations/data/ (empty when absent), else `tous-publics`.
"""

from pathlib import Path

from data_inclusion.schema.v1.publics import Public as DiPublic
from django.contrib.postgres.fields import ArrayField
from django.db import migrations, models

from dora.services.models import validate_corresponding_di_publics

DATA_DIR = Path(__file__).resolve().parent / "data"
TOUS_PUBLICS = DiPublic.TOUS_PUBLICS.value
VALID_DI_PUBLICS = {p.value for p in DiPublic}


def backfill_publics(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    updated = []
    qs = Service.objects.prefetch_related("publics").only("pk").iterator(chunk_size=500)
    for service in qs:
        slugs = set()
        precisions = []

        for public in service.publics.all():
            slugs.update(
                s
                for s in (public.corresponding_di_publics or [])
                if s in VALID_DI_PUBLICS
            )
            # Structure-specific custom names are preserved as free text.
            if public.structure_id is not None:
                precisions.append(public.name)

        # If service has no publics, put tous-publics
        if not slugs:
            slugs.add(TOUS_PUBLICS)

        # Exclusivity: tous-publics may not coexist with a specific public.
        if len(slugs) > 1:
            slugs.discard(TOUS_PUBLICS)

        service.publics_di = sorted(slugs)
        service.publics_precisions = ", ".join(dict.fromkeys(precisions))
        updated.append(service)

        if len(updated) >= 500:
            Service.objects.bulk_update(updated, ["publics_di", "publics_precisions"])
            updated = []

    if updated:
        Service.objects.bulk_update(updated, ["publics_di", "publics_precisions"])


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_protect_structure_fks"),
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
