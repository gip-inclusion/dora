from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0015_service_full_desc"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="description",
            field=models.TextField(
                blank=True, default="", max_length=10000, verbose_name="Description"
            ),
            preserve_default=False,
        ),
    ]
