# https://github.com/betagouv/itou/blob/master/config/settings/_sentry.py

import logging
import os

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration, ignore_logger


def strip_sentry_sensitive_data(event, hint):
    """
    Soyez très prudent de ne pas lever d'exception dans cette méthode,
    car quand cela arrive, l'erreur 500 initiale
    n'atteint jamais les serveurs sentry... et cela pourrait prendre
    des mois avant qu'on réalise qu'une vraie erreur a été silencée.
    De plus, vous ne pouvez pas utiliser le débogueur ici.
    """
    try:  # Envelopper tout dans try/catch pour plus de sécurité
        if "user" in event:
            # Malheureusement cela ne fonctionne pas pour l'adresse IP
            # qui continue d'apparaître. ¯\_(ツ)_/¯
            keys_to_delete_if_present = ["email", "username", "ip_address"]
            for key in keys_to_delete_if_present:
                event["user"].pop(key, None)  # Plus sûr que del
            # Identifier clairement les utilisateurs qui ne se sont pas connectés.
            if "id" not in event["user"]:
                event["user"]["id"] = "anonymous"

        # Corriger le problème d'adresse IP en filtrant les variables d'environnement de la requête
        if "request" in event and "env" in event["request"]:
            env = event["request"]["env"]
            ip_headers = [
                "REMOTE_ADDR",
                "HTTP_X_FORWARDED_FOR",
                "HTTP_X_REAL_IP",
                "HTTP_CLIENT_IP",
            ]
            for header in ip_headers:
                env.pop(header, None)

        # Filtrer les données sensibles des données de requête (paramètres POST, etc.)
        if "request" in event and "data" in event["request"]:
            data = event["request"]["data"]
            if isinstance(data, dict):
                sensitive_fields = {
                    "password",
                    "passwd",
                    "secret",
                    "token",
                    "api_key",
                    "csrf",
                }
                for key in list(data.keys()):
                    if any(sensitive in key.lower() for sensitive in sensitive_fields):
                        data[key] = "[Filtré]"

        # Filtrer les données sensibles des en-têtes de requête
        if "request" in event and "headers" in event["request"]:
            headers = event["request"]["headers"]
            sensitive_headers = {
                "authorization",
                "cookie",
                "x-api-key",
                "x-auth-token",
                "x-csrf-token",
            }
            for header in list(headers.keys()):
                if header.lower() in sensitive_headers:
                    headers[header] = "[Filtré]"

        # Filtrer les données sensibles des breadcrumbs
        if "breadcrumbs" in event:
            for breadcrumb in event["breadcrumbs"]:
                if "data" in breadcrumb and isinstance(breadcrumb["data"], dict):
                    data = breadcrumb["data"]
                    sensitive_fields = {
                        "password",
                        "passwd",
                        "secret",
                        "token",
                        "api_key",
                    }
                    for key in list(data.keys()):
                        if any(
                            sensitive in key.lower() for sensitive in sensitive_fields
                        ):
                            data[key] = "[Filtré]"

        return event
    except Exception:
        # Si quelque chose échoue, retourner l'événement original
        # Mieux vaut envoyer des données sensibles que perdre l'erreur
        return event


sentry_logging = LoggingIntegration(
    level=logging.INFO,  # Capturer info et plus comme breadcrumbs.
    event_level=logging.WARNING,  # Envoyer les avertissements comme événements.
)


def sentry_init(dsn):
    try:
        traces_sample_rate = float(os.getenv("SENTRY_TRACES_SAMPLE_RATE", ""))
    except ValueError:
        traces_sample_rate = 0

    # Obtenir le taux d'échantillonnage des profils (pour le profilage de performance)
    try:
        profiles_sample_rate = float(os.getenv("SENTRY_PROFILES_SAMPLE_RATE", ""))
    except ValueError:
        profiles_sample_rate = 0

    sentry_sdk.init(
        dsn=dsn,
        integrations=[
            sentry_logging,
            DjangoIntegration(),
        ],
        # Définir traces_sample_rate à 1.0 pour capturer 100%
        # des transactions pour le monitoring de performance.
        # Nous recommandons d'ajuster cette valeur en production.
        traces_sample_rate=traces_sample_rate,
        # Activer le profilage de performance
        profiles_sample_rate=profiles_sample_rate,
        # Associer les utilisateurs (ID+email+nom d'utilisateur+IP) aux erreurs.
        # https://docs.sentry.io/platforms/python/django/
        send_default_pii=True,
        # Filtrer l'email et le nom d'utilisateur sensibles.
        # L'adresse IP est maintenant filtrée dans la fonction before_send.
        # https://docs.sentry.io/error-reporting/configuration/filtering/?platform=python
        before_send=strip_sentry_sensitive_data,
        # Ajouter le suivi de release pour un meilleur débogage
        release=os.getenv("SENTRY_RELEASE"),
        # Ajouter l'environnement pour le filtrage
        environment=os.getenv("ENVIRONMENT", "unknown"),
        # Ignorer les erreurs de bruit communes
        ignore_errors=[
            "ConnectionResetError",
            "ConnectionAbortedError",
            "BrokenPipeError",
            "DisallowedHost",  # Déjà ignoré dans les logs mais bon d'avoir ici aussi
            "SuspiciousOperation",
        ],
        # Limiter les breadcrumbs pour réduire la taille de la charge utile
        max_breadcrumbs=50,
        # Ajouter des traces de pile à tous les événements pour un meilleur débogage
        attach_stacktrace=True,
        # La solution alternative
        # https://docs.sentry.io/enriching-error-data/additional-data/?platform=python#capturing-the-user
        # ne fonctionne que ici (sans accès à `request.user`)
        # et est silencieusement ignorée quand utilisée dans `context_processors.py` pour accéder à `request.user`.
    )
    ignore_logger("django.security.DisallowedHost")
    ignore_logger("django_datadog_logger.middleware.request_log")
