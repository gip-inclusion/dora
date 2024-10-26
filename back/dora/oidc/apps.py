from django.apps import AppConfig

"""
dora.oidc:
    Gère les connexions OIDC-Connect via ProConnect.
    Basée sur un provider custom de django-allauth.
    Remplace l'ancien système de connexion à Inclusion-Connect à partir de novembre 2024.
"""


class OIDCConfig(AppConfig):
    name = "dora.oidc"
    verbose_name = "Gestion des connexions ProConnect"
