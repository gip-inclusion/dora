import django.contrib.postgres.fields
from django.db import migrations, models


def fill_kinds(apps, schema_editor):
    """Reprend les types de service depuis la table M2M vers `ServiceKind`."""
    SearchView = apps.get_model("stats", "SearchView")

    rows = list(
        SearchView.objects.filter(kinds__isnull=False)
        .distinct()
        .prefetch_related("kinds")
    )
    for row in rows:
        row.kinds_tmp = sorted(kind.value for kind in row.kinds.all())

    SearchView.objects.bulk_update(rows, ["kinds_tmp"], batch_size=1000)


def restore_kinds(apps, schema_editor):
    SearchView = apps.get_model("stats", "SearchView")
    ServiceKind = apps.get_model("services", "ServiceKind")

    kind_ids = dict(ServiceKind.objects.values_list("value", "id"))
    through = SearchView.kinds.through

    through.objects.bulk_create(
        [
            through(searchview_id=row.pk, servicekind_id=kind_ids[value])
            for row in SearchView.objects.exclude(kinds_tmp=[])
            for value in row.kinds_tmp
            if value in kind_ids
        ],
        batch_size=1000,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("stats", "0004_searchview_region"),
    ]

    operations = [
        migrations.AddField(
            model_name="searchview",
            name="kinds_tmp",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("accompagnement", "Accompagnement"),
                        ("aide-financiere", "Aide financière"),
                        ("aide-materielle", "Aide materielle"),
                        ("atelier", "Atelier"),
                        ("formation", "Formation"),
                        ("information", "Information"),
                    ],
                    max_length=255,
                ),
                blank=True,
                default=list,
                size=None,
                verbose_name="Types de service",
            ),
        ),
        migrations.RunPython(fill_kinds, restore_kinds),
        migrations.RemoveField(
            model_name="searchview",
            name="kinds",
        ),
        migrations.RenameField(
            model_name="searchview",
            old_name="kinds_tmp",
            new_name="kinds",
        ),
    ]
