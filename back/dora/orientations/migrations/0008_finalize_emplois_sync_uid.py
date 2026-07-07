import uuid

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("orientations", "0007_backfill_emplois_sync_uid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="emploisorientationdata",
            name="emplois_sync_uid",
            field=models.UUIDField(
                default=uuid.uuid4,
                editable=False,
                unique=True,
                verbose_name="Emplois sync UID",
            ),
        ),
    ]
