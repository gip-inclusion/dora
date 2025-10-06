import logging

from django.db import migrations

structure_sources_to_rename = (
    ("api-referentiel-agences-pole-emploi", "api-referentiel-agences-france-travail"),
    ("dr-dt-pole-emploi", "dr-dt-france-travail"),
)

logger = logging.getLogger(__name__)


def rename_structure_sources(apps, schema_editor):
    StructureSource = apps.get_model("structures", "StructureSource")

    for old_value, new_value in structure_sources_to_rename:
        try:
            source = StructureSource.objects.get(value=old_value)
        except StructureSource.DoesNotExist:
            logger.error(f"StructureSource {old_value} does not exist")

        source.value = new_value
        source.save()

        logger.info(f"StructureSource {old_value} renamed to {new_value}")


class Migration(migrations.Migration):
    dependencies = [
        ("structures", "0076_rename_code_safir_pe_structure_code_safir_ft"),
    ]

    operations = [
        migrations.RunPython(
            rename_structure_sources, reverse_code=migrations.RunPython.noop
        ),
    ]
