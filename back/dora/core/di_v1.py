"""Migration logic for DI v1 fields.

For every new field or set of fields:
1. Add the necessary schema migration (AddField only, no data migration)
2. Extend sync_v1_service_fields() or sync_v1_structure_fields() below
3. Add tests
4. Backfill existing rows after deploy with backfill_di_v1 --wet-run
"""

SERVICE_DI_V1_FIELDS = []
STRUCTURE_DI_V1_FIELDS = []


def sync_v1_service_fields(service, *, save=True):
    if save and SERVICE_DI_V1_FIELDS:
        service.save(update_fields=SERVICE_DI_V1_FIELDS)


def sync_v1_structure_fields(structure, *, save=True):
    if save and STRUCTURE_DI_V1_FIELDS:
        structure.save(update_fields=STRUCTURE_DI_V1_FIELDS)
