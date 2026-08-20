"""Suppression du résumé, désormais dérivé de la description.

Le contenu des deux champs a été fusionné par la commande `merge_service_descriptions`
lancée en one-off juste avant ce déploiement.
"""

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0011_service_description"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="short_desc",
        ),
    ]
