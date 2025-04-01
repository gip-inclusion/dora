import mozilla_django_oidc.urls  # noqa: F401
from django.urls import path

import dora.oidc.views as views

oidc_patterns = [
    # les patterns internes pour le callback et le logout sont définis
    # dans le fichier `urls.py` de mozilla_django_oidc
    # redirection vers ProConnect pour la connexion
    path("oidc/login/", views.oidc_login, name="oidc_login"),
    # redirection une fois la connexion terminée
    path("oidc/logged_in/", views.oidc_logged_in, name="oidc_logged_in"),
    # preparation au logout : 2 étapes nécessaires
    # l'une de déconnexion sur ProConnect, l'autre locale de destruction de la session active
    path("oidc/pre_logout/", views.oidc_pre_logout, name="oidc_pre_logout"),
    # la plupart des vues de `mozilla-django-oidc` sont paramètrables
    # pas le logout
    path("oidc/logout/", views.CustomLogoutView.as_view(), name="oidc_logout"),
]
