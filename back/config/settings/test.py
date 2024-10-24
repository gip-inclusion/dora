import os

import dj_database_url

from .base import *  # noqa F403

DEBUG = True

# Base de données :
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

if DATABASE_URL := os.getenv("DATABASE_URL"):
    # utilisation de DATABASE_URL si défini, mais sans SSL
    DATABASES = {"default": dj_database_url.config()}
else:
    # sinon configuration "traditionnelle" de postgres
    DATABASES = {
        "default": {
            "NAME": os.getenv("POSTGRES_DB", "dora"),
            "USER": os.getenv("POSTGRES_USER", "dora"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("POSTGRES_HOST", "localhost"),
            "PORT": os.getenv("POSTGRES_PORT", "5432"),
        }
    }

# Ne pas oublier de redéfinir le moteur après une modification de config DB
DATABASES["default"]["ENGINE"] = "django.contrib.gis.db.backends.postgis"

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "192.168.0.1", "0.0.0.0"]
AUTH_PASSWORD_VALIDATORS = []

# Configuration nécessaire pour les tests :
SIB_ACTIVE = False

# Nécessaire pour la C.I. : fixe des valeurs par défaut pour les conteneurs
# faire correspondre les valeurs définies dans la configuration de la CI
CORS_ALLOWED_ORIGIN_REGEXES = [os.getenv("DJANGO_CORS_ALLOWED_ORIGIN_REGEXES", "*")]
FRONTEND_URL = os.getenv("FRONTEND_URL", "http://localhost:3000")
IC_TOKEN_URL = os.getenv("IC_TOKEN_URL", "https://whatever-oidc-token-url.com")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "dora")
SIB_ONBOARDING_LIST = os.getenv("SIB_ONBOARDING_LIST", "1")
SIB_ONBOARDING_PUTATIVE_MEMBER_LIST = os.getenv(
    "SIB_ONBOARDING_PUTATIVE_MEMBER_LIST", "2"
)
SIB_ONBOARDING_MEMBER_LIST = os.getenv("SIB_ONBOARDING_MEMBER_LIST", "3")
