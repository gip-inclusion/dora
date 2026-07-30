"""Utilitaires de lecture de la configuration depuis l'environnement.

Ce module est importé par les settings : il ne doit dépendre que de la
bibliothèque standard (pas de Django, dont la configuration n'est pas encore
chargée à ce moment-là).
"""

import os


def env_list(name: str, default: str = "") -> list[str]:
    """Lit une liste de valeurs séparées par des virgules.

    Les espaces entourant les valeurs sont ignorés, ainsi que les valeurs vides
    (variable non définie, chaîne vide, virgules superflues).
    """
    return [
        value.strip() for value in os.getenv(name, default).split(",") if value.strip()
    ]


def env_set(name: str, default: str = "") -> frozenset[str]:
    """Comme `env_list`, pour les réglages dont on ne teste que l'appartenance.

    À réserver aux cas où l'ordre et les doublons n'ont pas de sens (listes
    d'autorisation ou d'exclusion) : préférer `env_list` si le réglage est
    indexé ou parcouru dans l'ordre.
    """
    return frozenset(env_list(name, default))
