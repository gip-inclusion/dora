import logging
from urllib.parse import urlparse

from django.conf import settings
from django.core.exceptions import SuspiciousOperation
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from furl import furl
from itoutils.urls import add_url_params
from mozilla_django_oidc.views import (
    OIDCAuthenticationCallbackView,
    OIDCAuthenticationRequestView,
    OIDCLogoutView,
    resolve_url,
)
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes

from dora.core.constants import FRONTEND_PC_CALLBACK_URL

logger = logging.getLogger(__name__)


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def oidc_login(request):
    # Simple redirection vers la page d'identification ProConnect (si pas identifié)
    return HttpResponseRedirect(
        redirect_to=reverse("oidc_authentication_init")
        + f"?{request.META.get('QUERY_STRING')}"
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def oidc_logged_in(request):
    # Étape indispensable pour le passage du token au frontend_state :
    # malheureusement, cette étape est "zappée" si un paramètre `next` est passé lors de l'identification
    # `mozilla-django-oidc` ne le prends pas en compte, il faut pour modifier la vue de callback et le redirect final

    # attention : l'utilisateur est toujours anonyme (à ce point il n'existe qu'un token DRF)
    token = Token.objects.get(user_id=request.session["_auth_user_id"])

    redirect_uri = FRONTEND_PC_CALLBACK_URL

    # gestion du `next` :
    if request.GET.get("next"):
        redirect_uri = add_url_params(redirect_uri, request.GET)

    # Passage au front des informations complémentaires de l'utilisateur
    # ici : SAFIR et / ou SIRET
    if siret_safir := request.session.pop("_siret_safir", None):
        url_params = token.user.structure_to_join(
            siret=siret_safir["siret"], safir=siret_safir["safir"]
        )
        redirect_uri = add_url_params(redirect_uri, url_params)

    response = HttpResponseRedirect(redirect_to=redirect_uri)

    cookie_kwargs = {
        "path": "/",
        "samesite": "Lax",
        "secure": True,
        "httponly": False,
    }

    parsed_frontend_url = urlparse(settings.FRONTEND_URL)
    cookie_kwargs["domain"] = parsed_frontend_url.hostname

    response.set_cookie("token", token.key, **cookie_kwargs)

    return response


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def oidc_pre_logout(request):
    # attention : le nom oidc_logout est pris par mozilla-django-oidc
    # récupération du token stocké en session:
    if oidc_token := request.session.get("oidc_id_token"):
        # ProConnect nécessite un `state` pour vérifier la déconnexion effective
        logout_state = get_random_string(32)
        request.session["logout_state"] = logout_state
        params = {
            "id_token_hint": oidc_token,
            "state": logout_state,
            "post_logout_redirect_uri": request.build_absolute_uri(
                reverse("oidc_logout")
            ),
        }
        logout_url = furl(settings.OIDC_OP_LOGOUT_ENDPOINT, args=params)
        return HttpResponseRedirect(redirect_to=logout_url.url)

    # Si il n'y a pas de token OIDC présent en session,
    # il est aussi possible que la session soit active suite à une connexion
    # via "magic link", auquel cas un autre token est présent.
    if not request.session.get(settings.SESAME_SESSION_NAME):
        # Si il ne s'agit pas d'une connexion 'sesame', il s'agit d'une déconnexion
        # d'un utilisateur connecté via Inclusion Connect.
        # Ce cas disparaitra progressivement.
        logging.warning("Tentative de déconnexion sans token ou lien magique (IC?)")

    # Dans tous les cas, effacement de la session Django :
    return HttpResponseRedirect(redirect_to=reverse("oidc_logout"))


class CustomAuthenticationRequestView(OIDCAuthenticationRequestView):
    """
    Vue d'authentification OIDC personnalisée :
        Surcharge la vue par défaut de `mozilla-django-oidc` pour ajouter
        le paramètre `login_hint` à la requête d'autorisation si celui-ci
        est présent dans les paramètres de la requête HTTP.
    """

    def get_extra_params(self, request):
        extra_params = super().get_extra_params(request) or {}

        login_hint = request.GET.get("login_hint")
        if login_hint:
            extra_params["login_hint"] = login_hint

        return extra_params


class CustomAuthorizationCallbackView(OIDCAuthenticationCallbackView):
    """
    Callback OIDC :
        Vue personnalisée basée en grande partie sur celle définie par `mozilla-django-oidc`,
        pour la gestion du retour OIDC après identification.

        La gestion du `next_url` par la classe par défaut n'est pas satisfaisante dans le contexte de DORA,
        la redirection vers le frontend nécessitant une étape supplémentaire pour l'enregistrement du token DRF.
        Cette classe modifie la dernière redirection du flow pour y ajouter le paramètre d'URL suivant,
        plutôt que d'effectuer une redirection directement vers ce paramètre.

        A noter qu'il est trés simple de modifier les différentes étapes du flow OIDC pour les adapter,
        `mozilla-django-oidc` disposant d'une série de settings pour spécifier les classes de vue à utiliser
        pour chaque étape OIDC (dans ce cas via le setting `OIDC_CALLBACK_CLASS`).
    """

    @property
    def success_url(self):
        # récupération du paramètre d'URL suivant stocké en session en début de flow OIDC

        next_url = self.request.session.get("oidc_login_next", None)
        next_fieldname = self.get_settings("OIDC_REDIRECT_FIELD_NAME", "next")

        success_url = resolve_url(self.get_settings("LOGIN_REDIRECT_URL"))
        success_url += f"?{next_fieldname}={next_url}" if next_url else ""

        # redirection vers le front via `oidc/logged_in`
        return success_url

    @property
    def failure_url(self):
        logger.error("Erreur d'identification, redirection vers la page d'accueil")

        return self.get_settings("LOGIN_REDIRECT_URL_FAILURE")


class CustomLogoutView(OIDCLogoutView):
    """
    Logout OIDC :
        ProConnect effectue des vérifications avant de déconnecter l'utilisateur
        sur sa plateforme.
        Essentiellement en vérifiant la validité d'un `state` passé en paramètre
        avant la destruction de la session.
        Cette classe effectue simplement la vérification du `state` précédemment stocké
        en session (voir `oidc/pre_logout`) et réutilise la classe de vue originale
        de `mozilla-django-oidc`.
    """

    def post(self, request):
        if logout_state := request.session.pop("logout_state", None):
            if request.GET.get("state") != logout_state:
                raise SuspiciousOperation("La vérification de la déconnexion a échoué")
        elif not request.session.get(settings.SESAME_SESSION_NAME):
            # jeter une erreur ici est un peu violent, on se contentera d'un warning
            logger.warning("Vérification de la déconnexion impossible (lien direct)")

        return super().post(request)
