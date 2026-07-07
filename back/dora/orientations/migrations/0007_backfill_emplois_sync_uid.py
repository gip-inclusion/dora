import uuid

from django.db import migrations


def backfill_unique_uuids(apps, schema_editor):
    EmploisOrientationData = apps.get_model("orientations", "EmploisOrientationData")
    rows = list(EmploisOrientationData.objects.all().only("pk"))
    for row in rows:
        row.emplois_sync_uid = uuid.uuid4()
    if rows:
        EmploisOrientationData.objects.bulk_update(rows, ["emplois_sync_uid"])


class Migration(migrations.Migration):
    dependencies = [
        ("orientations", "0006_emploisorientationdata_emplois_sync_uid"),
    ]

    operations = [
        migrations.RunPython(backfill_unique_uuids, migrations.RunPython.noop),
    ]
