# Generated manually for Django 6.0 compatibility
#
# Django 6.0 breaking change: RenameField on ManyToManyField no longer automatically
# renames the through table.
#
# Migration 0124 renamed 'concerned_public' to 'publics', but in Django 6 this leaves
# the through table with the old name 'services_service_concerned_public'.
#
# This migration explicitly renames the M2M through table to its expected name.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0124_rename_concerned_public_service_publics"),
    ]

    operations = [
        migrations.RunSQL(
            # Rename M2M through table from concerned_public to publics
            sql=[
                'ALTER TABLE IF EXISTS "services_service_concerned_public" RENAME TO "services_service_publics";',
            ],
            # Reverse SQL to undo the rename
            reverse_sql=[
                'ALTER TABLE IF EXISTS "services_service_publics" RENAME TO "services_service_concerned_public";',
            ],
        ),
    ]
