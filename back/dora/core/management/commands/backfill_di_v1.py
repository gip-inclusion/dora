"""Backfill DI v1 fields on existing services and structures.

Schema migrations only create empty columns; this command populates them
from legacy Dora fields (orientation modes, typology, national labels, …).
"""

import logging

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.core.di_v1 import (
    SERVICE_DI_V1_FIELDS,
    STRUCTURE_DI_V1_FIELDS,
    sync_v1_service_fields,
    sync_v1_structure_fields,
)
from dora.services.models import Service
from dora.structures.models import Structure

logger = logging.getLogger("dora.logs.core")
BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    """Populate DI v1 fields after deploy (replaces data migrations)."""

    ATOMIC_HANDLE = True

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")
        scope = parser.add_mutually_exclusive_group()
        scope.add_argument(
            "--structures",
            action="store_true",
            help="Backfill structures only",
        )
        scope.add_argument(
            "--services",
            action="store_true",
            help="Backfill services only",
        )

    @dry_runnable
    def handle(self, *args, **options):
        if not options["services"]:
            self._backfill_queryset(
                Structure._base_manager.prefetch_related("national_labels"),
                sync_v1_structure_fields,
                STRUCTURE_DI_V1_FIELDS,
            )
        if not options["structures"]:
            self._backfill_queryset(
                Service._base_manager.prefetch_related(
                    "coach_orientation_modes",
                    "beneficiaries_access_modes",
                ),
                sync_v1_service_fields,
                SERVICE_DI_V1_FIELDS,
            )

    def _backfill_queryset(self, queryset, sync_fn, fields):
        updated = []
        n_rows = 0
        model = queryset.model
        for obj in queryset.iterator(chunk_size=BATCH):
            sync_fn(obj, save=False)
            updated.append(obj)
            if len(updated) >= BATCH:
                model._base_manager.bulk_update(updated, fields)
                n_rows += len(updated)
                logger.info("%d rows processed", n_rows)
                updated = []
        if updated:
            model._base_manager.bulk_update(updated, fields)
            n_rows += len(updated)
            logger.info("%d rows processed", n_rows)
