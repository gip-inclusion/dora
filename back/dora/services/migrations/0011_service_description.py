"""Fusion des deux champs de présentation d'un service en un champ `description` unique.

Renommage plutôt que création : les descriptifs déjà rédigés restent en place. `max_length`
sur un `TextField` n'étant pas une contrainte SQL, les rares dépassements sont conservés.
"""

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0010_recompute_sync_checksums_publics"),
    ]

    operations = [
        migrations.RenameField(
            model_name="service",
            old_name="full_desc",
            new_name="description",
        ),
        migrations.AlterField(
            model_name="service",
            name="description",
            field=models.TextField(
                blank=True, max_length=10000, verbose_name="Description"
            ),
        ),
    ]
