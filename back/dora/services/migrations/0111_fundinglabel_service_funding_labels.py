# Generated by Django 4.2.16 on 2024-10-31 16:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0110_remove_service_fee_pass_numerique"),
    ]

    operations = [
        migrations.CreateModel(
            name="FundingLabel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("value", models.CharField(db_index=True, max_length=255, unique=True)),
                ("label", models.CharField(max_length=255)),
            ],
            options={
                "verbose_name": "Label de financement",
                "verbose_name_plural": "Labels de financement",
            },
        ),
        migrations.AddField(
            model_name="service",
            name="funding_labels",
            field=models.ManyToManyField(
                blank=True,
                to="services.fundinglabel",
                verbose_name="Labels de financement",
            ),
        ),
    ]