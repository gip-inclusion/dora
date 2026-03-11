from django.db import models


class MainActivity(models.TextChoices):
    ACCOMPAGNATEUR = "accompagnateur", "Accompagnateur"
    OFFREUR = "offreur", "Offreur"
    ACCOMPAGNATEUR_OFFREUR = "accompagnateur_offreur", "Accompagnateur et offreur"
    AUTRE = "autre", "Autre"


class DiscoveryMethod(models.TextChoices):
    BOUCHE_A_OREILLE = (
        "bouche-a-oreille",
        "Bouche-à-oreille (mes collègues, réseau, etc.)",
    )
    MOTEURS_DE_RECHERCHE = (
        "moteurs-de-recherche",
        "Moteurs de recherche (Ecosia, Qwant, Google, Bing, etc.)",
    )
    RESEAUX_SOCIAUX = "reseaux-sociaux", "Réseaux sociaux (Linkedin, Twitter, etc.)"
    EVENEMENTS_DORA = (
        "evenements-dora",
        "Événements DORA (démonstration, webinaires, open labs, etc.)",
    )
    EMPLOIS_DE_L_INCLUSION = (
        "emplois-de-l-inclusion",
        "Emplois de l'inclusion",
    )
    AUTRE = "autre", "Autre (préciser)"
