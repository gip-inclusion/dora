from django.db import migrations

# Suppression de l'ancienne application « admin_express », entièrement
# remplacée par « decoupage_administratif ».

DROP_TABLES_SQL = """
DROP TABLE IF EXISTS admin_express_city;
DROP TABLE IF EXISTS admin_express_department;
DROP TABLE IF EXISTS admin_express_epci;
DROP TABLE IF EXISTS admin_express_region;
DELETE FROM django_migrations WHERE app = 'admin_express';
"""


class Migration(migrations.Migration):
    dependencies = [
        ("decoupage_administratif", "0002_add_overseas_departments"),
    ]

    operations = [
        migrations.RunSQL(DROP_TABLES_SQL, reverse_sql=migrations.RunSQL.noop),
    ]
