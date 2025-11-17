import logging

from django.conf import settings
from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from rest_framework.authtoken.models import Token
from sesame.utils import get_token, get_user

from dora.auth_links.emails import send_authentication_link
from dora.auth_links.enums import AuthLinkAction
from dora.core.constants import FRONTEND_PC_CALLBACK_URL
from dora.users.models import User

logger = logging.getLogger("dora.logs.core")

# TODO:
# suite à la suppression d'inclusion-connect,
# la connexion directe par lien est-elle toujours utilisée ?


@csrf_exempt
@require_http_methods(["POST"])
def send_link(request):
    # on ne veut que des utilisateurs qui se sont déjà connectés via IC
    user = get_object_or_404(
        User,
        email=request.POST.get("email"),
        is_active=True,
        is_valid=True,
    )

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

    return HttpResponse(status=204)


def authenticate_with_link(request, sesame):
    if sesame:
        if user := get_user(sesame):
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

            redirect_uri = f"{FRONTEND_PC_CALLBACK_URL}#{token.key}"
            return HttpResponseRedirect(redirect_uri)

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
