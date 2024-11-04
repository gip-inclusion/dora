# Hack :
# `dora.oidc` n'était pas censé devenir une app à part entière,
# mais pour ajouter des management command, une app Django correctement configurée est nécessaire.
# Placer le backend d'identification dans l'`__init__.py` empêche l'initialisation de Django (cycle dans les apps),
# il faut donc le renommer et le placer par exemple dans un module `backends`.
# Mais ...
# `mozilla-django-oidc` à la *très* mauvaise idée de stocker dans la session le nom de la classe de backend :
# si on change l'emplacement de cette dernière, toutes les sessions actives auront en session un mauvais nom de classe,
# et à chaque interaction avec OIDC, l'app plante lamentablement.
# D'ou ce hack un peu crade qui permet de faire dynamiquement pointer `dora.oidc.OIDCAuthenticationBackend`
# vers `dora.oidc.backends.OIDCAuthenticationBackend` (swizzle).
# D'habitude on fait ça avec une variable `__all__`, mais le comportement n'est pas dynamique.

# FIXME:
# une solution possible une fois que les connexions OIDC à ProConnect seront "battle-tested",
# sera (en weekend par ex.):
# - de virer ce hack,
# - de le passer en prod,
# - de virer toutes les sessions utilisateurs.
# Les sessions seront recréés au fil de l'eau avec la bonne classe en session.


def __getattr__(name):
    if name == "OIDCAuthenticationBackend":
        from .backends import OIDCAuthenticationBackend  # noqa

        return OIDCAuthenticationBackend

    raise AttributeError(f"module '{__name__}' has no attribute '{name}'")
