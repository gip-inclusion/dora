from data_inclusion.schema import Typologie

"""
Valeurs métiers communes à l'app 'dora.structure'.
Aurait eu sa place dans un module `enums`, mais désormais DORA réutilise
autant que possible les énumérations du schéma D·I.
"""


# On indique ici les typologies qui ne doivent pas être modifiables par l'utilisateur.
RESTRICTED_STRUCTURE_TYPOLOGIES = (Typologie.FT,)

# On indique ici les labels nationaux faisant l'objet d'une curation
# et de restrictions particulières (FT, CapEmploi, partenaires régionaux).
# Note / TODO :
# ce sont des `EnumModel`, donc pas de typage.
# Il serait intéressant de les avoir sous forme de fixture.
RESTRICTED_NATIONAL_LABELS = ("adie", "cap-emploi-reseau-cheops", "france-travail")
