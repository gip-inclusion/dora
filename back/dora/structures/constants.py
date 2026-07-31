from dora.data_inclusion.enums import TypologieStructure

"""
Valeurs métiers communes à l'app 'dora.structure'.
Aurait eu sa place dans un module `enums`, mais désormais DORA réutilise
autant que possible les énumérations du schéma D·I.
"""


# On indique ici les typologies qui ne doivent pas être modifiables par l'utilisateur.
RESTRICTED_STRUCTURE_TYPOLOGIES = (TypologieStructure.FT,)

TYPOLOGIES_EXCLUDED_FROM_AWAITING_ACTIVATION = (
    TypologieStructure.ACI,
    TypologieStructure.AI,
    TypologieStructure.CAARUD,
    TypologieStructure.CADA,
    TypologieStructure.CCAS,
    TypologieStructure.CHRS,
    TypologieStructure.CHU,
    TypologieStructure.CPH,
    TypologieStructure.CSAPA,
    TypologieStructure.EA,
    TypologieStructure.EATT,
    TypologieStructure.EI,
    TypologieStructure.ETTI,
    TypologieStructure.FT,
    TypologieStructure.GEIQ,
    TypologieStructure.HUDA,
    TypologieStructure.OIL,
    TypologieStructure.PJJ,
    TypologieStructure.SPIP,
)

# On indique ici les labels nationaux faisant l'objet d'une curation
# et de restrictions particulières (FT, CapEmploi, partenaires régionaux, SIAE).
# Note / TODO :
# ce sont des `EnumModel`, donc pas de typage.
# Il serait intéressant de les avoir sous forme de fixture.
RESTRICTED_NATIONAL_LABELS = (
    "adie",
    "cap-emploi-reseau-cheops",
    "conseil-departemental",
    "france-travail",
    "siae",
)
