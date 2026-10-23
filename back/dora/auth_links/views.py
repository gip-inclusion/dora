import logging

from django.conf import settings
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from itoutils.urls import add_url_params
from rest_framework.authtoken.models import Token
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
    throttle_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from sesame.utils import get_token, get_user

from dora.auth_links.emails import send_authentication_link
from dora.auth_links.enums import AuthLinkAction
from dora.auth_links.utils import generate_auth_code
from dora.core.constants import FRONTEND_CALLBACK_URL
from dora.core.throttling import AuthLinkEmailThrottle, AuthLinkIpThrottle
from dora.users.models import User

logger = logging.getLogger("dora.logs.core")

# TODO:
# suite à la suppression d'inclusion-connect,
# la connexion directe par lien est-elle toujours utilisée ?


# Vue DRF pour bénéficier du throttling ; sans authentification, donc sans CSRF.
@api_view(["POST"])
@authentication_classes([])
@permission_classes([AllowAny])
@throttle_classes([AuthLinkIpThrottle, AuthLinkEmailThrottle])
def send_link(request: Request) -> Response:
    # on ne veut que des utilisateurs qui se sont déjà connectés via IC
    user = User.objects.filter(
        email=request.data.get("email"),
        is_active=True,
        is_valid=True,
    ).first()

    # Même réponse que le compte existe ou non, pour ne pas permettre l'énumération
    if user is None:
        return Response(status=204)

    magic_link = get_token(user)
    url = request.build_absolute_uri(
        reverse("authenticate_with_link", kwargs={"sesame": magic_link})
    )

    send_authentication_link(user.email, url)

    logger.info(
        "Demande de connexion par lien direct",
        {
            "legal": True,
            "action": AuthLinkAction.SENT_AUTH_LINK,
            "userId": user.pk,
            "userEmail": user.email,
        },
    )

    return Response(status=204)


def authenticate_with_link(request, sesame):
    if sesame:
        if user := get_user(sesame):
            # un élément du script sync-analytics.sh dépend de ce log, notamment du message et de la clé userId du payload.
            logger.info(
                "Connexion par lien direct",
                {
                    "legal": True,
                    "action": AuthLinkAction.DID_AUTHENTICATE_WITH_AUTH_LINK,
                    "userId": user.pk,
                    "userEmail": user.email,
                },
            )
            token, _ = Token.objects.get_or_create(user=user)

            # on garde une trace de la connexion par lien magique
            # pour ne pas effectuer le flow de déconnexion OIDC en entier
            request.session[settings.SESAME_SESSION_NAME] = True

            # Échange sécurisé via un code à usage unique
            code = generate_auth_code(token.key)

            return HttpResponseRedirect(
                add_url_params(FRONTEND_CALLBACK_URL, {"code": code})
            )

    logger.warning(
        "Lien direct invalide ou expiré",
        {
            "action": AuthLinkAction.USED_EXPIRED_AUTH_LINK,
            "sesameLink": f"...{sesame[:-5]}",
        },
    )

    # le lien est invalide ou expiré :
    # redirection vers l'accueil (à défaut d'une page d'erreur)
    return HttpResponseRedirect(settings.FRONTEND_URL)
