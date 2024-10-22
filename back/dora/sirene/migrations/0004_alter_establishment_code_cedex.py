from django.db import migrations
from django.db.models.functions import Length


def strip_cedex(apps, schema_editor):
    Establishment = apps.get_model("sirene", "Establishment")
    for est in Establishment.objects.annotate(cedex_length=Length("code_cedex")).filter(
        cedex_length__gt=5
    ):
        est.code_cedex = est.code_cedex[:5]
        est.save()


class Migration(migrations.Migration):
    dependencies = [
        ("sirene", "0003_establishment_is_social"),
    ]

    operations = [
        migrations.RunPython(strip_cedex),
    ]
