import hmac

from django.conf import settings
from rest_framework.settings import api_settings
from rest_framework.throttling import (
    AnonRateThrottle,
    SimpleRateThrottle,
    UserRateThrottle,
)


def get_front_client_ip(request) -> str | None:
    """IP du client transmise par le front, si elle est accompagnée du secret partagé.

    Pour les requêtes du front (proxy `/api` et SSR), la dernière adresse de
    `X-Forwarded-For` est celle du front, commune à tous les visiteurs.
    """
    secret = settings.FRONT_PROXY_SECRET
    received = request.META.get("HTTP_X_DORA_PROXY_SECRET", "")
    # Utilisation de `hmac.compare_digest` pour éviter les attaques temporelles.
    if secret and hmac.compare_digest(received.encode(), secret.encode()):
        return request.META.get("HTTP_X_DORA_CLIENT_IP", "").strip() or None
    return None


def get_client_ip(request) -> str | None:
    """IP réelle du client, non falsifiable par celui-ci.

    Pour les requêtes du front, l'IP qu'il transmet ; sinon, l'adresse ajoutée
    par le routeur Scalingo à la fin de `X-Forwarded-For` (même règle que DRF
    avec `NUM_PROXIES`) : les adresses précédentes sont fournies par le client.
    """
    if front_client_ip := get_front_client_ip(request):
        return front_client_ip
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    num_proxies = api_settings.NUM_PROXIES
    if xff and num_proxies:
        addrs = xff.split(",")
        return addrs[-min(num_proxies, len(addrs))].strip() or None
    return request.META.get("REMOTE_ADDR") or None


class ClientIpAnonRateThrottle(AnonRateThrottle):
    def get_ident(self, request):
        return get_front_client_ip(request) or super().get_ident(request)


class ClientIpUserRateThrottle(UserRateThrottle):
    def get_ident(self, request):
        return get_front_client_ip(request) or super().get_ident(request)


class UploadRateThrottle(ClientIpUserRateThrottle):
    """Throttle spécifique pour les endpoints du chargement de fichiers."""

    scope = "upload"


class OrientationsExportLinkThrottle(ClientIpUserRateThrottle):
    """Throttle pour l'envoi par e-mail du lien d'export des orientations."""

    scope = "orientations_export_link"


class AuthLinkIpThrottle(ClientIpAnonRateThrottle):
    """Throttle par IP pour la demande de lien de connexion (énumération de comptes)."""

    scope = "auth_link_ip"


class AuthLinkEmailThrottle(SimpleRateThrottle):
    """Throttle par adresse e-mail pour la demande de lien de connexion.

    Limite l'envoi répété de liens à une même adresse, y compris depuis plusieurs IP.
    """

    scope = "auth_link_email"

    def get_cache_key(self, request, view):
        email = str(request.data.get("email", "")).strip().lower()
        if not email:
            return None
        return self.cache_format % {"scope": self.scope, "ident": email}


class StructureUploadThrottle(SimpleRateThrottle):
    """Throttle par structure pour éviter l'abus d'une structure compromise."""

    scope = "structure_upload"

    def get_cache_key(self, request, view):
        structure_slug = request.resolver_match.kwargs["structure_slug"]
        return self.cache_format % {"scope": self.scope, "ident": structure_slug}
