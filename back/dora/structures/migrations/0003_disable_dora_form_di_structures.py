from django.db import migrations

DISABLED_STRUCTURES = [
    "dora--53b97c59-3409-4124-9669-cf27bdb50fa7",
    "dora--53be817e-69d5-4833-bbcf-1f20baecec47",
    "dora--66c27f67-75de-4cb9-99f5-dfdf80295135",
    "dora--681db8d1-b9f0-42f1-9a8c-176670e588fb",
    "dora--6f76b8f0-bac7-4480-ae73-49d0713609bf",
    "dora--719100f4-8859-40b6-a08e-f480f3271d3a",
    "dora--78cea06a-e6c0-4743-8d41-f9e98d873bd5",
    "dora--8f42afda-ea59-4a2b-93dd-7f0ec2e72c47",
    "dora--9186590f-90ea-4d47-885c-745f00ba8d54",
    "dora--aa584caa-0c7d-4b31-a41a-97cb5cbd99b9",
    "dora--b535b26f-b5c4-4b80-84c1-66611886b106",
    "dora--bbaa573d-f40b-493e-9dde-d343cf80865a",
    "dora--c1dc91f1-47e7-45ea-a811-efadbddb3339",
    "dora--c513fdf5-b774-4472-a265-1d78b3156674",
    "dora--c690a761-5dae-40fa-83b0-a97cafa2fd93",
    "dora--d4ce0cad-a60f-4776-b146-34df54ee9252",
    "dora--d5181961-0c59-46aa-9b0a-4d2b1fdaf44d",
    "dora--e174dc0d-3153-4486-988c-bb7375890d89",
    "dora--e71fc379-5ed5-4ba0-8548-d7237a939374",
    "dora--ed3f9b5c-907a-49b2-9dc0-3d811777bf81",
    "dora--ed405ca1-138f-478e-b568-68258c699187",
    "dora--f0d44c57-ddcf-46ca-a301-19f829d3e615",
    "dora--fea6604e-a482-4944-a0ac-5ac162b51433",
    "fredo--97407_13040",
    "fredo--97407_13043",
    "fredo--97407_13111",
    "fredo--97407_13194",
    "fredo--97407_13202",
    "fredo--97407_14547",
    "fredo--97416_12872",
    "fredo--97416_13123",
    "fredo--97416_13436",
    "carif-oref--04_141",
    "dora--89b257fd-9562-4177-a0e5-5bb41114cef0",
    "mediation-numerique--Coop-numérique_a52fa51d-6e91-4b73-9ef0-b34df981e1be",
    "carif-oref--24_1140523",
    "dora--02ed489a-cf21-44f1-98da-3b90ac748c0a",
    "dora--065581cc-d261-4c3a-b47d-1326d8c8ff94",
    "dora--1d235830-0359-4eec-a7c7-94950ec5224a",
    "dora--2664e2a9-5437-450e-8253-a694b5a61816",
    "dora--2aa64295-aa89-44e1-ae1e-12e261e50c53",
    "dora--2d1ec461-558f-4d62-b466-77918e3dc936",
    "dora--38adaf62-85fb-497d-9193-2c4939a8ab4a",
    "dora--39e058d6-7830-42c6-98c7-059fa13a9dd9",
    "dora--3a77aed6-c8ea-47fa-bf09-aba9162dae66",
    "dora--3c2195e6-e3b3-4bcf-8bfb-bf1c01337e8b",
    "dora--3e16cd2b-f075-48e7-ac2f-cfe2b40167fd",
    "dora--4de39ebb-3a3d-4337-9db4-763ee07f77a6",
    "dora--4fd22e78-a22b-46c1-a3a8-4890b5fde942",
]


def add_disabled_structures(apps, schema_editor):
    DisabledDoraFormDIStructure = apps.get_model(
        "structures", "DisabledDoraFormDIStructure"
    )
    for entry in DISABLED_STRUCTURES:
        source, structure_id = entry.split("--", 1)
        DisabledDoraFormDIStructure.objects.get_or_create(
            source=source,
            structure_id=structure_id,
            defaults={"comment": "CAF"},
        )


def remove_disabled_structures(apps, schema_editor):
    DisabledDoraFormDIStructure = apps.get_model(
        "structures", "DisabledDoraFormDIStructure"
    )
    for entry in DISABLED_STRUCTURES:
        source, structure_id = entry.split("--", 1)
        DisabledDoraFormDIStructure.objects.filter(
            source=source, structure_id=structure_id, comment="CAF"
        ).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0002_seed_data"),
    ]

    operations = [
        migrations.RunPython(
            add_disabled_structures,
            reverse_code=remove_disabled_structures,
        ),
    ]
