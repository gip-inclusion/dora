from collections import defaultdict

from data_inclusion.schema.v1 import ModeMobilisation

# À une thématique DI correspond une thématique Dora
THEMATIQUES_MAPPING_DI_TO_DORA = {
    "logement-hebergement--etre-accompagne-dans-son-projet-accession": "logement-hebergement--etre-accompagne-pour-se-loger",
    "logement-hebergement--etre-accompagne-en cas-de-difficultes-financieres": "logement-hebergement--gerer-son-budget",
    "logement-hebergement--financer-son-projet-travaux": "logement-hebergement--autre",
}

# Inversion du dictionnaire
# À une thématique Dora correspond une liste de thématiques DI
THEMATIQUES_MAPPING_DORA_TO_DI = defaultdict(list)
for key, value in THEMATIQUES_MAPPING_DI_TO_DORA.items():
    THEMATIQUES_MAPPING_DORA_TO_DI[value].append(key)

MODE_MOBILISATION_DI_TO_DORA = {
    ModeMobilisation.ENVOYER_UN_COURRIEL: "envoyer-un-mail",
    ModeMobilisation.SE_PRESENTER: "se-presenter",
    ModeMobilisation.TELEPHONER: "telephoner",
    ModeMobilisation.UTILISER_LIEN_MOBILISATION: "completer-le-formulaire-dadhesion",
}
