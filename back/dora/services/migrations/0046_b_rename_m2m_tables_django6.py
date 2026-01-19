# Generated manually for Django 6.0 compatibility
#
# Django 6.0 breaking change: RenameField on ManyToManyField no longer automatically
# renames the through table.
#
# - Migration 0046 renamed fields ending in '2', leaving through tables with '2' suffix
# - Migration 0124 renamed 'concerned_public' to 'publics', leaving the old table name
#
# This migration explicitly renames all M2M through tables to their expected names.

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0046_auto_20220308_1754"),
    ]

    operations = [
        migrations.RunSQL(
            # Rename M2M through tables to remove '2' suffix
            sql=[
                'ALTER TABLE IF EXISTS "services_service_beneficiaries_access_modes2" RENAME TO "services_service_beneficiaries_access_modes";',
                'ALTER TABLE IF EXISTS "services_service_categories2" RENAME TO "services_service_categories";',
                'ALTER TABLE IF EXISTS "services_service_coach_orientation_modes2" RENAME TO "services_service_coach_orientation_modes";',
                'ALTER TABLE IF EXISTS "services_service_kinds2" RENAME TO "services_service_kinds";',
                'ALTER TABLE IF EXISTS "services_service_location_kinds2" RENAME TO "services_service_location_kinds";',
                'ALTER TABLE IF EXISTS "services_service_subcategories2" RENAME TO "services_service_subcategories";',
            ],
            # Reverse SQL to undo the rename
            reverse_sql=[
                'ALTER TABLE IF EXISTS "services_service_beneficiaries_access_modes" RENAME TO "services_service_beneficiaries_access_modes2";',
                'ALTER TABLE IF EXISTS "services_service_categories" RENAME TO "services_service_categories2";',
                'ALTER TABLE IF EXISTS "services_service_coach_orientation_modes" RENAME TO "services_service_coach_orientation_modes2";',
                'ALTER TABLE IF EXISTS "services_service_kinds" RENAME TO "services_service_kinds2";',
                'ALTER TABLE IF EXISTS "services_service_location_kinds" RENAME TO "services_service_location_kinds2";',
                'ALTER TABLE IF EXISTS "services_service_subcategories" RENAME TO "services_service_subcategories2";',
            ],
        ),
    ]
