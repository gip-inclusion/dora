import os

import dj_database_url

from .base import *  # noqa F403

DEBUG = True

# Base de données :
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DATABASE_URL:  # noqa 405
    # utilisation de `DATABASE_URL` si défini, mais sans SSL pour un environnement local
    DATABASES = {"default": dj_database_url.config()}
else:
    # sinon configuration "traditionnelle" de postgres
    DATABASES = {
        "default": {
            "NAME": os.getenv("POSTGRES_DB"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST"),
            "PORT": os.getenv("POSTGRES_PORT"),
        }
    }

# Ne pas oublier de redéfinir le moteur après une modification de config DB
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

# Django extensions :
INSTALLED_APPS += ["django_extensions"]  # noqa F405

# ALLOWED_HOSTS:
# fixé par variable d'environnement, hôtes séparés par des virgules et sans espace
# ou si absent : valeurs par défaut usuelles pour un environnement de dev.
if allowed_hosts := os.getenv("ALLOWED_HOSTS"):
    ALLOWED_HOSTS = allowed_hosts.split(",")
else:
    ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.0.1", "0.0.0.0"]

# Validation des formats de mots de passe :
# pas nécessaire pour un environnement de dev, peut éventuellement être
# modifié dans un environnement de test / custom / local
AUTH_PASSWORD_VALIDATORS = []

REST_FRAMEWORK["DEFAULT_RENDERER_CLASSES"] += (  # noqa F405
    "rest_framework.renderers.BrowsableAPIRenderer",
)

# Don't use json formatter in dev
del LOGGING["handlers"]["console"]["formatter"]  # noqa: F405

# Profiling :
# utilisation de Silk (configurable via var env)
PROFILE = os.getenv("DJANGO_PROFILE") == "true"

if DEBUG and PROFILE:
    SILKY_PYTHON_PROFILER = True
    INSTALLED_APPS.append("silk")  # noqa F405
    MIDDLEWARE = [
        "silk.middleware.SilkyMiddleware",
        "querycount.middleware.QueryCountMiddleware",
    ] + MIDDLEWARE  # noqa
    QUERYCOUNT = {
        "IGNORE_SQL_PATTERNS": [r"silk_"],
        "IGNORE_REQUEST_PATTERNS": [r"/silk/"],
    }
    globals().setdefault("CONTENT_SECURITY_POLICY", {}).setdefault(
        "EXCLUDE_URL_PREFIXES", []
    ).append("/silk/")

# TODO: nécessaire sur staging ?
# ce paramètre n'était fixé que pour les environnement *HORS* production
# Q : est-ce c'est justifié pour staging ?
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

LOGGING["loggers"]["django"]["level"] = os.getenv("DJANGO_LOG_LEVEL", "INFO")  # noqa F405
