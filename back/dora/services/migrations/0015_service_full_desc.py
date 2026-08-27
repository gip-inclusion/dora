from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0014_mobilisation_fields"),
    ]

    operations = [
        migrations.RenameField(
            model_name="service",
            old_name="description",
            new_name="full_desc",
        ),
        migrations.AlterField(
            model_name="service",
            name="full_desc",
            field=models.TextField(
                blank=True, verbose_name="Descriptif complet de l’offre"
            ),
        ),
    ]
