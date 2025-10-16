import logging

from django.conf import settings
from rest_framework.throttling import AnonRateThrottle

logger = logging.getLogger(__name__)


class ClientIPAnonRateThrottle(AnonRateThrottle):
    @staticmethod
    def get_client_ip(request):
        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            # X-Forwarded-For peut contenir plusieurs IPs : "client, proxy1, proxy2"
            # Le premier IP est le client originel
            ip = x_forwarded_for.split(",")[0].strip()
        else:
            ip = request.META.get("REMOTE_ADDR")

        if not x_forwarded_for and not settings.DEBUG:
            logger.error(
                "L'en-tête X-Forwarded-For est manquante. Assurez que le load balancer est bien configuré."
            )

        return ip

    def get_cache_key(self, request, view):
        if request.user.is_authenticated:
            return None

        ident = self.get_client_ip(request)
        return self.cache_format % {"scope": self.scope, "ident": ident}
