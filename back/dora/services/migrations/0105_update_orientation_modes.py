from django.conf import settings
from django.db import migrations
from django.db.models import Q

from dora.services.enums import ServiceStatus


def is_orientable(service):
    structure_blacklisted = False

    # La récupération de la structure du service échoue sur staging à cause de structures non-référencées.
    # Ce ne devrait pas être possible grâce aux contraintes d'intégrité, mais c'est pourtant le cas.
    # => la base de staging est moisie
    # Après vérification, la base de production n'est pas impactée par le problème (ouf).
    # 2 options :
    # - modifier le code et ajouter un garde qui sera inutile en production,
    # - modifier "à la main" les bases de données (staging et recette).
    # J'opte pour la première option, pour avoir un suivi et éventuellement retirer ce garde une fois
    # cette PR mise en production.
    try:
        structure = service.structure
    except Exception:
        # On considère que le service n'est pas orientable
        return False

    if siret := structure.siret:
        structure_blacklisted = siret[0:9] in settings.ORIENTATION_SIRENE_BLACKLIST

    return (
        service.status == ServiceStatus.PUBLISHED
        and not structure.disable_orientation_form
        and not structure_blacklisted
        and service.contact_email
        and (
            service.coach_orientation_modes.filter(
                Q(value="envoyer-courriel") | Q(value="envoyer-fiche-prescription")
            ).exists()
            or service.beneficiaries_access_modes.filter(
                value="envoyer-courriel"
            ).exists()
        )
    )


def replace_envoyer_formulaire_with_envoyer_courriel(CoachOrientationMode):
    envoyer_formulaire = CoachOrientationMode.objects.get(value="envoyer-formulaire")
    envoyer_courriel = CoachOrientationMode.objects.get(value="envoyer-courriel")

    services = envoyer_formulaire.service_set.all()

    for service in services:
        service.coach_orientation_modes.remove(envoyer_formulaire)
        service.coach_orientation_modes.add(envoyer_courriel)

    envoyer_formulaire.delete()


def add_new_coach_orientation_modes(CoachOrientationMode):
    CoachOrientationMode(
        value="formulaire-dora",
        label="Via le formulaire DORA",
    ).save()

    CoachOrientationMode(
        value="formulaire-externe",
        label="Via notre propre formulaire/site internet",
    ).save()


def reword_coach_orientation_mode_labels(CoachOrientationMode):
    CoachOrientationMode.objects.filter(value="envoyer-courriel").update(
        label="Nous envoyer un e-mail"
    )
    CoachOrientationMode.objects.filter(value="envoyer-fiche-prescription").update(
        label="Nous envoyer un e-mail avec une fiche de prescription"
    )
    CoachOrientationMode.objects.filter(value="telephoner").update(
        label="Nous téléphoner"
    )
    CoachOrientationMode.objects.filter(value="autre").update(
        label="Autre modalité (préciser)"
    )


def set_formulaire_dora_for_orientable_services(CoachOrientationMode, Service):
    formulaire_dora = CoachOrientationMode.objects.get(value="formulaire-dora")

    for service in Service.objects.all():
        if is_orientable(service):
            service.coach_orientation_modes.add(formulaire_dora)


def add_new_beneficiary_access_modes(BeneficiaryAccessMode):
    BeneficiaryAccessMode(
        value="professionnel",
        label="Se faire orienter par un professionnel",
    ).save()

    BeneficiaryAccessMode(
        value="formulaire-externe",
        label="Via notre propre formulaire/site internet",
    ).save()


def reword_beneficiary_access_mode_labels(BeneficiaryAccessMode):
    BeneficiaryAccessMode.objects.filter(value="envoyer-courriel").update(
        label="Nous envoyer un e-mail"
    )
    BeneficiaryAccessMode.objects.filter(value="telephoner").update(
        label="Nous téléphoner"
    )
    BeneficiaryAccessMode.objects.filter(value="autre").update(
        label="Autre modalité (préciser)"
    )


def update_orientation_modes(apps, schema_editor):
    Service = apps.get_model("services", "Service")
    CoachOrientationMode = apps.get_model("services", "CoachOrientationMode")
    BeneficiaryAccessMode = apps.get_model("services", "BeneficiaryAccessMode")

    # Modalités accompagnateur
    add_new_coach_orientation_modes(CoachOrientationMode)
    reword_coach_orientation_mode_labels(CoachOrientationMode)
    set_formulaire_dora_for_orientable_services(CoachOrientationMode, Service)
    replace_envoyer_formulaire_with_envoyer_courriel(CoachOrientationMode)

    # Modalités bénéficiaire
    add_new_beneficiary_access_modes(BeneficiaryAccessMode)
    reword_beneficiary_access_mode_labels(BeneficiaryAccessMode)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0104_service_appointment_link"),
    ]

    operations = [
        migrations.RunPython(
            update_orientation_modes, reverse_code=migrations.RunPython.noop
        ),
    ]
