from data_inclusion.schema.base import EnhancedEnum
from django.db import models


class ServiceStatus(models.TextChoices):
    SUGGESTION = "SUGGESTION", "Suggestion"
    DRAFT = "DRAFT", "Draft"
    PUBLISHED = "PUBLISHED", "Published"
    ARCHIVED = "ARCHIVED", "Archived"


# TODO: supprimer ce champ
class ServiceUpdateStatus(models.TextChoices):
    NEEDED = "NEEDED", "Actualisation conseillée"
    NOT_NEEDED = "NOT_NEEDED", "Service à jour"
    REQUIRED = "REQUIRED", "Actualisation exigée"


# TEMPORAIRE : à supprimer et utiliser l'enum de data-inclusion-schema quand la version avec l'option tous-publics sera publiée
class Public(EnhancedEnum):
    """Publics"""

    TOUS_PUBLICS = (
        "tous-publics",
        "Tous publics",
        "Tous publics",
    )

    ACTIFS = (
        "actifs",
        "Actifs",
        "Toute personne ayant un emploi, qu’il soit salarié, libéral ou à son compte",
    )
    BENEFICIAIRES_DES_MINIMAS_SOCIAUX = (
        "beneficiaires-des-minimas-sociaux",
        "Bénéficiaires des minimas sociaux",
        (
            "Personnes touchant des aides financières telles que RSA, SMIC, allocations"
            " familiales, bourses, etc"
        ),
    )
    DEMANDEURS_EMPLOI = (
        "demandeurs-emploi",
        "Demandeurs d’emploi",
        "Demandeurs d’emploi de tout type",
    )
    ETUDIANTS = (
        "etudiants",
        "Étudiants",
        "Étudiants",
    )
    FAMILLES = (
        "familles",
        "Familles",
        "Familles, parents, enfants, etc",
    )
    FEMMES = (
        "femmes",
        "Femmes",
        "Femmes isolées, victimes de violence, etc",
    )
    JEUNES = (
        "jeunes",
        "Jeunes",
        "Jeunes au sens large, jeunes adultes, adolescents, etc",
    )
    PERSONNES_EN_SITUATION_DE_HANDICAP = (
        "personnes-en-situation-de-handicap",
        "Personnes en situation de handicap",
        "Personnes en situation de handicap de tout type",
    )
    PERSONNES_EN_SITUATION_D_URGENCE = (
        "personnes-en-situation-durgence",
        "Personnes en situation d’urgence",
        "SDF, victimes de violence, grande précarité, etc",
    )
    PERSONNES_EN_SITUATION_JURIDIQUE_SPECIFIQUE = (
        "personnes-en-situation-juridique-specifique",
        "Personnes en situation juridique spécifique",
        "Personnes sortant de détention, détenus ou autre statut juridique spécifique",
    )
    PERSONNES_EXILEES = (
        "personnes-exilees",
        "Personnes exilées",
        "Réfugiés, demandeurs d’asile, personnes immigrées, etc",
    )
    RESIDENTS_QPV_FRR = (
        "residents-qpv-frr",
        "Résidents en QPV ou FRR",
        (
            "Personnes résidentes en zone Quartier Prioritaire de la Ville ou France"
            " Ruralités Revitalisation (anciennement ZRR)"
        ),
    )
    SENIORS = (
        "seniors",
        "Séniors",
        "Personnes âgées, retraités, etc",
    )
