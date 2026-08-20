from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0014_mobilisation_fields"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="service",
            name="short_desc",
        ),
    ]
