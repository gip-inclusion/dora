from django.db import migrations


def _load_v1_enum_referentiels(apps):
    """Crée les objets ServiceFee, LocationKind, ServiceKind de base."""
    from data_inclusion.schema.v1 import Frais, ModeAccueil, TypeService

    for model_name, enum_class in [
        ("ServiceFee", Frais),
        ("LocationKind", ModeAccueil),
        ("ServiceKind", TypeService),
    ]:
        model = apps.get_model("services", model_name)
        for item in enum_class:
            model.objects.get_or_create(value=item.value, label=item.label)


def _load_coach_orientation_modes(apps):
    """Crée les objets CoachOrientationMode de base."""
    CoachOrientationMode = apps.get_model("services", "CoachOrientationMode")
    coach_modes = [
        ("autre", "Autre modalité (préciser)"),
        ("envoyer-un-mail", "Nous envoyer un e-mail"),
        (
            "envoyer-un-mail-avec-une-fiche-de-prescription",
            "Nous envoyer un e-mail avec une fiche de prescription",
        ),
        ("telephoner", "Nous téléphoner"),
        ("formulaire-dora", "Via le formulaire DORA"),
        (
            "completer-le-formulaire-dadhesion",
            "Via notre propre formulaire en ligne/site internet",
        ),
    ]
    for value, label in coach_modes:
        CoachOrientationMode.objects.get_or_create(value=value, label=label)


def _load_beneficiary_access_modes(apps):
    """Crée les objets BeneficiaryAccessMode de base."""
    BeneficiaryAccessMode = apps.get_model("services", "BeneficiaryAccessMode")
    access_modes = [
        ("autre", "Autre modalité (préciser)"),
        ("envoyer-un-mail", "Nous envoyer un e-mail"),
        ("telephoner", "Nous téléphoner"),
        ("professionnel", "Se faire orienter par un professionnel"),
        ("se-presenter", "Se présenter"),
        (
            "completer-le-formulaire-dadhesion",
            "Via notre propre formulaire en ligne/site internet",
        ),
    ]
    for value, label in access_modes:
        BeneficiaryAccessMode.objects.get_or_create(value=value, label=label)


def _load_funding_labels(apps):
    """Crée les objets FundingLabel de base."""
    FundingLabel = apps.get_model("services", "FundingLabel")
    funding_labels = [
        ("cd-charente-maritime", "Conseil départemental de la Charente-Maritime"),
        ("cd-drome", "Conseil départemental de la Drôme"),
        ("cd-savoie", "Conseil départemental de la Savoie"),
        ("cd-aveyron", "Conseil départemental de l'Aveyron"),
        ("cd-vienne", "Conseil départemental de la Vienne"),
        ("cd-essonne", "Conseil Départemental de l'Essonne"),
        ("cd-bouches-du-rhone", "Conseil départemental des Bouches-du-Rhône"),
        ("rg-reunion", "Région Réunion"),
    ]
    for value, label in funding_labels:
        FundingLabel.objects.get_or_create(value=value, label=label)


def _load_access_conditions(apps):
    """Crée les objets AccessCondition de base."""
    AccessCondition = apps.get_model("services", "AccessCondition")
    access_conditions = [
        "Personnes n'ayant pas accès au crédit bancaire classique",
        "Orientable uniquement par le Conseil Départemental",
        "Sans logement / mal logé",
        "Personne non imposable",
        "Résident QPV / ZFRR",
        "Inscrit à la Mission Locale",
        "Salarié d'une SIAE",
        "Être éligible aux critères IAE",
        "Bénéficiaire d'un accompagnement PLIE",
        "Allocataire CAF",
        "Bénéficiaires de l'accompagnement global",
        "Entrée en formation d'au moins 40 heures",
        "Reprise d'emploi à temps plein ou temps partiel d'au moins 3 mois consécutifs",
        "Reconnaissance de la Commission des Droits et de l'Autonomie pour les Personnes Handicapées (CDAPH)",
        "Personne ne nécessitant pas de véhicule adapté",
        "Notification de transport adapté de la part de la M.D.P.H",
        "Demande du référent de l'enfant par un rapport circonstancié.",
        "Demande adressée par un travailleur social",
        "Locataire de votre résidence principale située sur le territoire français",
        "Salarié d'une entreprise du secteur privé non agricole",
        "Votre revenu ne dépasse pas 100% du SMIC",
        "Locataire de votre résidence principale à proximité de votre entreprise ou de votre lieu de formation",
        "Titulaire de la carte d'invalidité",
        "Exclu.e du système bancaire classique (faible revenu ou situation professionnelle fragile)",
        "Véhicule de moins de 200 000 km ou de moins de 15 ans",
        "L'entretien d'embauche ou l'emploi concernent un CDI, un CDD ou un contrat de travail temporaire d'au moins 3 mois consécutifs",
        "La distance doit être située à plus de 60 km aller-retour ou à plus de 2 heures aller-retour du lieu de résidence",
        "La formation doit être financée ou cofinancée par France Travail",
        "Etre adressé.e par un prescripteur partenaire",
        "Sous conditions de ressources",
        "Changer de logement ou en trouver un nouveau",
        "Contrat d’engagement",
    ]
    for name in access_conditions:
        AccessCondition.objects.get_or_create(name=name, structure=None)


def _load_requirements(apps):
    """Crée les objets Requirement de base."""
    Requirement = apps.get_model("services", "Requirement")
    requirements = [
        "Maitriser l'écriture, la lecture",
    ]
    for name in requirements:
        Requirement.objects.get_or_create(name=name, structure=None)


def _load_credentials(apps):
    """Crée les objets Credential de base."""
    Credential = apps.get_model("services", "Credential")
    credentials = [
        "Revenus fiscaux de référence figurant sur l'avis d'imposition de l'année n-2.",
        "Curriculum vitae",
        "Trois derniers bulletins de salaire",
        "Avis d'imposition",
        "Contrat de location ou bail",
        "Contrat d'apprentissage",
        "Justifier d'une carte d'invalidité",
        "Justificatif d'achat",
        "Justificatif coefficient familial (cf) inférieur à 950 euros",
        "Relevé d'informations restreint de la préfecture.",
        "Attestation précédente de l'assurance auto",
        "Justificatif d'entrée en formation",
        "Attestation sur l'honneur",
        "Carte grise du véhicule",
        "Contrat d'intégration Républicaine de - 24 mois",
        "Attestation Caisse Allocation Familiale (CAF)",
        "Attestation Reconnaissance Qualité Travailleur Handicapé",
        "Attestation Allocation Adulte Handicapé (AAH)",
        "Attestation Allocation Spécifique de Solidarité",
        "Attestation Revenu de Solidarité Active (RSA)",
        "Attestation d'inscription France Travail",
        "Copie du livret de famille ou acte de naissance",
        "Une copie des pièces d'identité des parents de ou des enfants",
        "Le carnet de santé du ou des enfants",
        "Le numéro d'allocataire Caisse Allocation Familiale (CAF)",
        "Justifier d'un garant",
        "Relevé d'identité Bancaire",
        "Justifier d'un entretien d'embauche à + de 60km aller/retour ou de 2h aller/retour du lieu de résidence",
        "Permis de conduire en cours de validité",
        "3 derniers relevés de compte bancaire",
        "Pièce d'identite en cours de validité",
        "Justificatif de ressource",
        "Justificatif de domicile de moins de 3 mois",
        "Projet de passer un concours validé",
        "Justifier d'un projet de formation validé",
        "3 derniers avis d'imposition",
        "Justifier d'une promesse d'embauche",
        "Justifier de 6 mois d'inscription en continu en tant que demandeur d'emploi",
        "Justificatif d'une embauche de +de 3 mois en Contrat à durée déterminée (CDD), Contrat à durée indéterminée (CDI), intérim",
        "Justifier d'une démarche d'insertion et de recherche d'emploi",
        "Suivi par un partenaire prescripteur",
    ]
    for name in credentials:
        Credential.objects.get_or_create(name=name, structure=None)


def _load_categories_and_subcategories(apps):
    """Crée les objets ServiceCategory et ServiceSubCategory de base."""
    from data_inclusion.schema.v0 import Thematique as ThematiqueV0
    from data_inclusion.schema.v1 import Categorie
    from data_inclusion.schema.v1 import Thematique as ThematiqueV1

    ServiceCategory = apps.get_model("services", "ServiceCategory")
    ServiceSubCategory = apps.get_model("services", "ServiceSubCategory")
    v1_subcategory_values = {t.value for t in ThematiqueV1}

    # Catégories v1
    for c in Categorie:
        ServiceCategory.objects.get_or_create(
            value=c.value,
            defaults={"label": c.label, "is_obsolete": False},
        )

    # Sous-catégories v1
    for t in ThematiqueV1:
        ServiceSubCategory.objects.get_or_create(
            value=t.value,
            defaults={"label": t.label, "is_obsolete": False},
        )

    # Sous-catégories v0 : créées uniquement si la valeur n’existe pas dans ThematiqueV1
    for t in ThematiqueV0:
        if t.value not in v1_subcategory_values:
            ServiceSubCategory.objects.get_or_create(
                value=t.value,
                defaults={"label": t.label, "is_obsolete": True},
            )

    # Catégories v0 uniquement (obsolètes, hors categorie v1)
    v0_only_category_values = {
        t.value.split("--")[0]
        for t in ThematiqueV0
        if t.value not in v1_subcategory_values
    }
    v1_category_values = {c.value for c in Categorie}
    obsolete_category_values = v0_only_category_values - v1_category_values
    for category_value in obsolete_category_values:
        category_label = category_value.replace("-", " ").title()
        ServiceCategory.objects.get_or_create(
            value=category_value,
            defaults={"label": category_label, "is_obsolete": True},
        )


def load_data_inclusion_referentiels(apps, schema_editor):
    _load_v1_enum_referentiels(apps)
    _load_coach_orientation_modes(apps)
    _load_beneficiary_access_modes(apps)
    _load_funding_labels(apps)
    _load_access_conditions(apps)
    _load_requirements(apps)
    _load_credentials(apps)
    _load_categories_and_subcategories(apps)


class Migration(migrations.Migration):
    dependencies = [
        ("services", "0002_initial"),
    ]

    operations = [
        migrations.RunPython(
            load_data_inclusion_referentiels, reverse_code=migrations.RunPython.noop
        ),
    ]
