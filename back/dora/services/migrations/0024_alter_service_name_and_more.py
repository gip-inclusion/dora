"""
Les migrations pour finaliser la transition vers le schema DI pour les services
1. Augmentation de la taille de la longueur maximale de `name` d'une service à 150
2. Le défaut des `zones_eligibilite` est une liste vide
3. Assurer que toutes les valeurs `None` ou `['france'] dans `zones_eligibilite` deviennent une liste vide
4. Mettre les valeurs stockés dans `publics_derived_from_conditions` dans `publics`
5. Ajout des validators pour `mobilisable_by`, `mobilisation_modes`, et `horaires_accueil`
"""

import django.contrib.postgres.fields
from data_inclusion.schema.v1.publics import Public as DiPublic
from django.db import migrations, models
from django.db.models import Q

import dora.core.validators

DI_PUBLICS_ORDER = {p.value: index for index, p in enumerate(DiPublic)}


def transform_national_eligibility_zones(apps, schema_editor):
    Service = apps.get_model("services", "Service")

    Service._base_manager.filter(
        Q(zone_eligibilite__contains=["france"]) | Q(zone_eligibilite__isnull=True)
    ).update(zone_eligibilite=[])


def normalize_publics(publics):
    # les valeurs inconnues du référentiel DI sont rejetées en fin de liste
    # plutôt que de faire échouer la migration
    return sorted(
        set(publics),
        key=lambda public: DI_PUBLICS_ORDER.get(public, len(DI_PUBLICS_ORDER)),
    )


def combine_publics_columns(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    services = (
        Service.objects.filter(publics_derived_from_conditions__len__gte=1)
        .only("id", "publics", "publics_derived_from_conditions")
        .iterator(chunk_size=1000)
    )

    updated_services = []
    for service in services:
        service.publics = normalize_publics(
            (service.publics or []) + service.publics_derived_from_conditions
        )
        updated_services.append(service)

    Service.objects.bulk_update(updated_services, ["publics"], batch_size=1000)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0023_remove_service_moderation"),
    ]

    operations = [
        migrations.AlterField(
            model_name="service",
            name="name",
            field=models.CharField(max_length=150, verbose_name="Nom de l’offre"),
        ),
        migrations.AlterField(
            model_name="service",
            name="zone_eligibilite",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(max_length=255),
                blank=True,
                default=list,
                null=True,
                verbose_name="Zone d’éligibilité",
            ),
        ),
        migrations.RunPython(
            transform_national_eligibility_zones, migrations.RunPython.noop
        ),
        migrations.RunPython(
            combine_publics_columns,
            migrations.RunPython.noop,
            elidable=True,
        ),
        migrations.AlterField(
            model_name="service",
            name="mobilisable_by",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("usagers", "Usagers"),
                        ("professionnels", "Professionnels"),
                    ],
                    max_length=255,
                ),
                blank=True,
                default=None,
                null=True,
                verbose_name="Mobilisable par",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="mobilisation_modes",
            field=django.contrib.postgres.fields.ArrayField(
                base_field=models.CharField(
                    choices=[
                        ("envoyer-un-courriel", "Envoyer un courriel"),
                        ("se-presenter", "Se présenter"),
                        ("telephoner", "Téléphoner"),
                        (
                            "utiliser-lien-mobilisation",
                            "Utiliser le lien de mobilisation",
                        ),
                    ],
                    max_length=255,
                ),
                blank=True,
                default=None,
                null=True,
                verbose_name="Modes de mobilisation",
            ),
        ),
        migrations.AlterField(
            model_name="service",
            name="horaires_accueil",
            field=models.CharField(
                blank=True,
                max_length=255,
                null=True,
                validators=[dora.core.validators.validate_opening_hours_str],
                verbose_name="Horaires d'accueil du public",
            ),
        ),
    ]
