# Generated by Django 3.2.5 on 2021-08-18 17:10

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0004_alter_service_structure"),
    ]

    operations = [
        migrations.AddField(
            model_name="service",
            name="slug",
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
    ]