from django.db import migrations
from django.db.models.functions import RTrim


def normalize_admin_division_name(apps, _):
    for model_name in ["City", "EPCI", "Department", "Region"]:
        model = apps.get_model("admin_express", model_name)
        model.objects.update(normalized_name=RTrim("normalized_name"))


class Migration(migrations.Migration):
    dependencies = [
        ("admin_express", "0005_auto_20220207_1209"),
    ]

    operations = [
        migrations.RunPython(normalize_admin_division_name, migrations.RunPython.noop)
    ]
