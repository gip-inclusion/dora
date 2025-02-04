from django.db import migrations


def add_label_conseil_departemental(apps, schema_editor):
    StructureNationalLabel = apps.get_model("structures", "StructureNationalLabel")

    if not StructureNationalLabel.objects.filter(
        value="conseil-departemental"
    ).exists():
        StructureNationalLabel.objects.create(
            value="conseil-departemental", label="Conseil départemental"
        )


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0072_alter_structure_name"),
    ]

    operations = [
        migrations.RunPython(add_label_conseil_departemental, migrations.RunPython.noop)
    ]
