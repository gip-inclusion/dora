from data_inclusion.schema.v1 import TypeService
from django.db import migrations

ARCHIVE_TABLE = "services_service_kinds_archive"


def archive_kinds(apps, schema_editor):
    """Archive la M2M avant sa suppression.

    Le passage à un type unique fait perdre les types secondaires d'environ 58 % des
    services : ils sont conservés quelques mois dans une table hors ORM, autonome (elle
    stocke la valeur du type et non l'identifiant de `ServiceKind`, qui disparaît ici).
    """
    with schema_editor.connection.cursor() as cursor:
        cursor.execute(
            f"""
            CREATE TABLE {ARCHIVE_TABLE} AS
            SELECT liaison.service_id, kind.value AS kind
            FROM services_service_kinds AS liaison
            JOIN services_servicekind AS kind ON kind.id = liaison.servicekind_id
            """
        )


def restore_kinds(apps, schema_editor):
    """Repeuple `ServiceKind` et la M2M depuis l'archive, puis la supprime."""
    ServiceKind = apps.get_model("services", "ServiceKind")
    Service = apps.get_model("services", "Service")

    ServiceKind.objects.bulk_create(
        [ServiceKind(value=t.value, label=t.label) for t in TypeService],
        ignore_conflicts=True,
    )
    kind_ids = dict(ServiceKind.objects.values_list("value", "id"))
    through = Service.kinds.through

    with schema_editor.connection.cursor() as cursor:
        cursor.execute(f"SELECT service_id, kind FROM {ARCHIVE_TABLE}")
        through.objects.bulk_create(
            [
                through(service_id=service_id, servicekind_id=kind_ids[value])
                for service_id, value in cursor.fetchall()
                if value in kind_ids
            ],
            batch_size=1000,
        )
        cursor.execute(f"DROP TABLE {ARCHIVE_TABLE}")


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0008_recompute_sync_checksums"),
        # dernière migration à référencer `ServiceKind` : sur une base neuve, elle doit
        # s'appliquer avant que le modèle ne disparaisse de l'état
        ("stats", "0005_searchview_kinds_array"),
    ]

    operations = [
        migrations.RunPython(archive_kinds, restore_kinds),
        migrations.RemoveField(
            model_name="service",
            name="kinds",
        ),
        migrations.DeleteModel(
            name="ServiceKind",
        ),
    ]
