from data_inclusion.schema.v1 import ReseauPorteur

"""
Valeurs métiers communes à l'app 'dora.structure'.
Aurait eu sa place dans un module `enums`, mais désormais DORA réutilise
autant que possible les énumérations du schéma D·I.
"""


# Réseaux porteurs dont les structures (SIAE) ne sont pas considérées
# « en attente d'activation » lorsqu'elles n'ont pas de service publié.
RESEAUX_PORTEURS_EXCLUDED_FROM_AWAITING_ACTIVATION = frozenset(
    reseau.value
    for reseau in (
        ReseauPorteur.ACI,
        ReseauPorteur.AI,
        ReseauPorteur.CAARUD,
        ReseauPorteur.CADA,
        ReseauPorteur.CCAS_CIAS,
        ReseauPorteur.CHRS,
        ReseauPorteur.CHU,
        ReseauPorteur.CPH,
        ReseauPorteur.CSAPA,
        ReseauPorteur.EI,
        ReseauPorteur.ETTI,
        ReseauPorteur.FRANCE_TRAVAIL,
        ReseauPorteur.GEIQ,
        ReseauPorteur.HUDA,
        ReseauPorteur.PJJ,
        ReseauPorteur.SPIP,
        ReseauPorteur.UNEA,
    )
)
