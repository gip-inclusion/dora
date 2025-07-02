import dj_database_url

from .base import *  # noqa F403
from .sentry import sentry_init

DEBUG = False

# Database : configuration de production
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

# Dans les environnements déployés sur Scalingo (prod, staging, review),
# seule la variable d'environnement DATABASE_URL est définie pour
# établir la connexion à la base de données.

if DATABASE_URL:  # noqa F405
    # SSL obligatoire pour la production
    DATABASES = {"default": dj_database_url.config(ssl_require=True)}
else:
    raise Exception(
        "Impossible de configurer la connexion à la base de données : DATABASE_URL absent"
    )

# Ne pas oublier de redéfinir le moteur après une modification de config DB
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"


# Sécurité (navigateur) :

CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
# Disabled as this is already managed by Scalingo
# also : raised as `security.W004` via `check --deploy`
# SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
# https://hstspreload.org/
# SECURE_HSTS_PRELOAD = True
# SECURE_BROWSER_XSS_FILTER = True : plus utilisé depuis Django 3.0
SECURE_REFERRER_POLICY = "same-origin"
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_SSL_REDIRECT = True

# Certains formulaires d'admin (par ex. structures)
# peuvent contenir un grand nombre de champs associés (par ex. membres)
# et déclencher une erreur de type : `TooManyFieldsSent` lors de la modification
# et de la validation des enregistrements.
DATA_UPLOAD_MAX_NUMBER_FIELDS = 4_000


# Sentry :
sentry_init()
