from django.db import migrations

OVERSEAS_DEPARTMENTS = [
    {
        "code": "975",
        "name": "Saint-Pierre-et-Miquelon",
        "normalized_name": "SAINT PIERRE ET MIQUELON",
    },
    {
        "code": "977",
        "name": "Saint-Barthélemy",
        "normalized_name": "SAINT BARTHELEMY",
    },
    {
        "code": "978",
        "name": "Saint-Martin",
        "normalized_name": "SAINT MARTIN",
    },
    {
        "code": "984",
        "name": "Terres australes et antarctiques françaises",
        "normalized_name": "TERRES AUSTRALES ET ANTARCTIQUES FRANCAISES",
    },
    {
        "code": "986",
        "name": "Wallis-et-Futuna",
        "normalized_name": "WALLIS ET FUTUNA",
    },
    {
        "code": "987",
        "name": "Polynésie française",
        "normalized_name": "POLYNESIE FRANCAISE",
    },
    {
        "code": "988",
        "name": "Nouvelle-Calédonie",
        "normalized_name": "NOUVELLE CALEDONIE",
    },
    {
        "code": "989",
        "name": "Île de Clipperton",
        "normalized_name": "ILE DE CLIPPERTON",
    },
]


def create_overseas_departments(apps, schema_editor):
    Department = apps.get_model("decoupage_administratif", "Department")
    for dept in OVERSEAS_DEPARTMENTS:
        Department.objects.update_or_create(
            code=dept["code"],
            defaults={
                "name": dept["name"],
                "normalized_name": dept["normalized_name"],
                # Les COMs n'ont pas de région au sens métropolitain :
                # par convention INSEE, on réutilise le code du territoire.
                "region": dept["code"],
            },
        )


def delete_overseas_departments(apps, schema_editor):
    Department = apps.get_model("decoupage_administratif", "Department")
    codes = [dept["code"] for dept in OVERSEAS_DEPARTMENTS]
    Department.objects.filter(code__in=codes).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("decoupage_administratif", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            create_overseas_departments,
            reverse_code=delete_overseas_departments,
        ),
    ]
