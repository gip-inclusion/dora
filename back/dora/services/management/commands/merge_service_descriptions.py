"""Réintégration du résumé des services dans leur description, le temps de la migration.

`Service.short_desc` disparaît au profit d'une description unique. Certains résumés complètent
la description — à conserver, en tête — et d'autres n'en sont qu'une recopie ou une paraphrase
— à jeter. Le tri est celui de `dora.services.descriptions`.
"""

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.descriptions import build_idf, is_blank, merge_description
from dora.services.models import Service
from dora.services.utils import (
    SYNC_CUSTOM_M2M_FIELDS,
    SYNC_M2M_FIELDS,
    update_sync_checksum,
)

BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    ATOMIC_HANDLE = True
    help = (
        "Réintègre le résumé des services dans leur description : en tête quand il la "
        "complète, abandonné quand il ne fait que la redire."
    )

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")

    @dry_runnable
    def handle(self, *args, **options):
        weight = build_idf(
            Service._base_manager.exclude(full_desc="")
            .values_list("full_desc", flat=True)
            .iterator(chunk_size=BATCH)
        )

        updated, touched_models = [], set()
        copied = dropped = inserted = 0

        services = (
            Service._base_manager.only("pk", "is_model", "short_desc", "full_desc")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for service in services:
            if not service.short_desc.strip():
                continue

            merged = merge_description(service.short_desc, service.full_desc, weight)
            if merged is None:
                dropped += 1
                continue

            if is_blank(service.full_desc):
                copied += 1
            else:
                inserted += 1

            service.full_desc = merged
            if service.is_model:
                touched_models.add(service.pk)
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["full_desc"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["full_desc"])

        self.stdout.write(f"{copied:>7} descriptions reprises du résumé")
        self.stdout.write(f"{inserted:>7} résumés insérés en tête de la description")
        self.stdout.write(
            f"{dropped:>7} résumés abandonnés, déjà dits par la description"
        )
        self.stdout.write(
            f"{self._recompute_sync_checksums(touched_models):>7} empreintes recalculées"
        )
        if not options["wet_run"]:
            self.stdout.write(
                self.style.WARNING("Dry-run : aucune modification enregistrée")
            )

    def _recompute_sync_checksums(self, model_ids: set) -> int:
        recomputed = 0
        updated = []
        models = (
            Service._base_manager.filter(pk__in=model_ids)
            .prefetch_related(*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS)
            .iterator(chunk_size=BATCH)
        )
        for model in models:
            previous = model.sync_checksum
            model.sync_checksum = update_sync_checksum(model)
            if model.sync_checksum == previous:
                continue

            # `last_sync_checksum=previous` : seules les copies restées en phase avec leur
            # modèle suivent, celles que leur structure a personnalisées gardent leur écart.
            Service._base_manager.filter(
                model_id=model.pk, last_sync_checksum=previous
            ).update(last_sync_checksum=model.sync_checksum)

            recomputed += 1
            updated.append(model)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["sync_checksum"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["sync_checksum"])

        return recomputed
