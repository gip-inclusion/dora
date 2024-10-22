# Generated by Django 3.2.5 on 2021-08-09 15:55

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="forms",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=1024),
                blank=True,
                default=list,
                size=None,
                verbose_name="Partagez les documents à compléter",
            ),
        ),
    ]