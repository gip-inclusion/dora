# Generated by Django 3.2.5 on 2021-08-26 08:04

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0013_auto_20210826_0958"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="beneficiaries_access_modes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("OS", "Se présenter"),
                        ("PH", "Téléphoner"),
                        ("EM", "Envoyer un mail"),
                        ("OT", "Autre (préciser)"),
                    ],
                    max_length=2,
                ),
                blank=True,
                default=list,
                size=None,
                verbose_name="Comment mobiliser la solution en tant que bénéficiaire",
            ),
        ),
    ]