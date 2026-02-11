from django.db import migrations


def forward(apps, schema_editor):
    AccessCondition = apps.get_model("services", "AccessCondition")

    AccessCondition.objects.filter(structure=None, name="Résident QPV / ZRR").update(
        name="Résident QPV / ZFRR"
    )


def backward(apps, schema_editor):
    AccessCondition = apps.get_model("services", "AccessCondition")

    AccessCondition.objects.filter(structure=None, name="Résident QPV / ZFRR").update(
        name="Résident QPV / ZRR"
    )


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0137_deprecate_ppae_and_cer_access_condition"),
    ]

    operations = [
        migrations.RunPython(forward, backward, elidable=True),
    ]
