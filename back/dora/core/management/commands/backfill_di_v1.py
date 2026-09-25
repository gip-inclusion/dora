"""Backfill DI v1 fields on existing services.

Schema migrations only create empty columns; this command populates them
from legacy Dora fields (orientation modes, access conditions, …).
"""

import logging

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.core.di_v1 import (
    SERVICE_DI_V1_FIELDS,
    SERVICE_SYNC_PREFETCHES,
    sync_v1_service_fields,
)
from dora.services.descriptions import backfill_service_descriptions
from dora.services.models import Service

logger = logging.getLogger("dora.logs.core")
BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    """Populate DI v1 fields after deploy (replaces data migrations)."""

    ATOMIC_HANDLE = True

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")

    @dry_runnable
    def handle(self, *args, **options):
        self._backfill_queryset(
            Service._base_manager.prefetch_related(*SERVICE_SYNC_PREFETCHES),
            sync_v1_service_fields,
            SERVICE_DI_V1_FIELDS,
        )
        backfill_service_descriptions(batch=BATCH)

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
