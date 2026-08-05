from data_inclusion.schema.v1 import ModeMobilisation as DiModeMobilisation
from data_inclusion.schema.v1 import PersonneMobilisatrice as DiPersonneMobilisatrice
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


# Valeurs reprises du schéma data·inclusion v1, mais redéclarées membre par
# membre : un `EnhancedEnum` passé en `choices` lève un `TypeError`, et
# `data-inclusion-schema` n'étant pas épinglé, en dériver le domaine de ces
# colonnes exposerait la base aux évolutions du paquet.
class ModeMobilisation(models.TextChoices):
    ENVOYER_UN_COURRIEL = (
        DiModeMobilisation.ENVOYER_UN_COURRIEL.value,
        DiModeMobilisation.ENVOYER_UN_COURRIEL.label,
    )
    SE_PRESENTER = (
        DiModeMobilisation.SE_PRESENTER.value,
        DiModeMobilisation.SE_PRESENTER.label,
    )
    TELEPHONER = (
        DiModeMobilisation.TELEPHONER.value,
        DiModeMobilisation.TELEPHONER.label,
    )
    UTILISER_LIEN_MOBILISATION = (
        DiModeMobilisation.UTILISER_LIEN_MOBILISATION.value,
        DiModeMobilisation.UTILISER_LIEN_MOBILISATION.label,
    )
    # Extension DORA : ce mode n'existe pas dans le schéma data·inclusion.
    FORMULAIRE_DORA = "formulaire-dora", "Via le formulaire DORA"


class PersonneMobilisatrice(models.TextChoices):
    USAGERS = (
        DiPersonneMobilisatrice.USAGERS.value,
        DiPersonneMobilisatrice.USAGERS.label,
    )
    PROFESSIONNELS = (
        DiPersonneMobilisatrice.PROFESSIONNELS.value,
        DiPersonneMobilisatrice.PROFESSIONNELS.label,
    )


DI_MODES_MOBILISATION = frozenset(mode.value for mode in DiModeMobilisation)

# Ordre canonique de sérialisation : les valeurs de `modes_mobilisation` et de
# `mobilisable_par` sont toujours triées selon cet ordre, faute de quoi une
# simple permutation modifierait le checksum de synchronisation des modèles.
# `update_sync_checksum` passant par `repr()`, ces champs doivent aussi ne
# contenir que des chaînes nues, jamais des membres d'enum.
MODES_MOBILISATION_ORDER = [mode.value for mode in ModeMobilisation]
MOBILISABLE_PAR_ORDER = [personne.value for personne in PersonneMobilisatrice]
