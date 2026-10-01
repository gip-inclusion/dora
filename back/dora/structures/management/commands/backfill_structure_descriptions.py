"""Fusion du résumé des structures dans leur description.

La composition réutilise celle des services (`dora.services.descriptions`) : le résumé est
repris en tête de la description, ou abandonné quand il ne fait que la redire. À lancer une
fois après le déploiement de la migration `structures.0007`, puis à supprimer avec
`short_desc`.
"""

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.descriptions import build_idf, derive_description
from dora.structures.models import Structure

BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    help = "Fusionne le résumé des structures (`short_desc`) dans leur description"
    ATOMIC_HANDLE = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Enregistre réellement les descriptions (sans ce flag, rollback automatique).",
        )

    @dry_runnable
    def handle(self, *args, **options):
        weight = build_idf(
            Structure.objects.exclude(description="")
            .values_list("description", flat=True)
            .iterator(chunk_size=BATCH)
        )

        stats = {"composed": 0, "copied": 0, "dropped": 0}
        updated = []
        structures = (
            Structure.objects.exclude(short_desc="")
            .only("pk", "short_desc", "description")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for structure in structures:
            description, reason = derive_description(
                structure.short_desc, structure.description, weight
            )
            if reason:
                stats[reason] += 1
            if description == structure.description:
                continue

            structure.description = description
            updated.append(structure)
            if len(updated) >= BATCH:
                Structure.objects.bulk_update(updated, ["description"])
                updated = []

        if updated:
            Structure.objects.bulk_update(updated, ["description"])

        self.logger.info(
            "Résumés repris en tête : %d, copiés dans une description vide : %d, "
            "abandonnés car redondants : %d",
            stats["composed"],
            stats["copied"],
            stats["dropped"],
        )
