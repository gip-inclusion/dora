import logging

from django.db import migrations

logger = logging.getLogger(__name__)


def forward(apps, schema_editor):
    AccessCondition = apps.get_model("services", "AccessCondition")
    ServiceAccessConditions = AccessCondition.service_set.through

    deprecated_access_conditions = AccessCondition.objects.filter(
        structure=None,
        name__in=[
            "Entrée en formation validée dans le cadre du Projet Personnalisé d’Accès à l’Emploi (PPAE)",
            "Personnes accompagnées dans le cadre d’un Contrat d’Engagement Réciproque (CER)",
        ],
    )
    new_access_condition = AccessCondition.objects.create(
        structure=None,
        name="Contrat d’engagement",
    )

    qs = ServiceAccessConditions.objects.filter(
        accesscondition__in=deprecated_access_conditions
    )

    new_m2m_objects = {}
    for link in qs:
        if link.service in new_m2m_objects:
            continue
        new_m2m_objects[link.service] = ServiceAccessConditions(
            accesscondition=new_access_condition, service=link.service
        )

    logger.info(
        "Création de %s nouvelles relations M2M pour remplacer les %s anciennes",
        len(new_m2m_objects),
        len(qs),
    )
    ServiceAccessConditions.objects.bulk_create(new_m2m_objects.values())
    deleted, _ = qs.delete()
    logger.info("%s anciennes relations M2M supprimées", deleted)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0136_migrate_diffusion_zones"),
    ]

    operations = [
        migrations.RunPython(
            forward, reverse_code=migrations.RunPython.noop, elidable=True
        ),
    ]
