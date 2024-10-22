from collections import defaultdict

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
