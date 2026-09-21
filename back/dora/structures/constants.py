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
