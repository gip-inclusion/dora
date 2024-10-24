import logging
import time

import jwt
import requests
from django.conf import settings
from django.core.cache import cache
from django.core.exceptions import SuspiciousOperation
from django.db import transaction
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.utils.crypto import get_random_string
from furl import furl
from mozilla_django_oidc.views import (
    OIDCAuthenticationCallbackView,
    OIDCLogoutView,
    resolve_url,
)
from rest_framework import permissions
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import APIException
from rest_framework.response import Response

from dora.rest_auth.views import update_last_login
from dora.users.models import User

from .utils import updated_ic_user


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def inclusion_connect_get_login_info(request):
    redirect_uri = request.data.get("redirect_uri")
    login_hint = request.data.get("login_hint", "")
    state = get_random_string(32)
    nonce = get_random_string(32)

    cache.set(
        f"oidc-state-{state}",
        {"state": state, "nonce": nonce, "redirect_uri": redirect_uri},
    )
    query = {
        "response_type": "code",
        "from": "dora",
        "client_id": {settings.IC_CLIENT_ID},
        "scope": "openid profile email",
        "nonce": nonce,
        "state": state,
        "redirect_uri": redirect_uri,
        "login_hint": login_hint,
    }
    return Response(
        {
            "url": furl(settings.IC_AUTH_URL).add(query).url,
            "state": state,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def inclusion_connect_get_logout_info(request):
    redirect_uri = request.data.get("redirect_uri")

    query = {
        "from": "dora",
        "client_id": {settings.IC_CLIENT_ID},
        "post_logout_redirect_uri": redirect_uri,
    }
    return Response(
        {
            "url": furl(settings.IC_LOGOUT_URL).add(query).url,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def inclusion_connect_get_update_info(request):
    referrer_uri = request.data.get("referrer_uri")
    login_hint = request.data.get("login_hint", "")

    query = {
        "from": "dora",
        "referrer": {settings.IC_CLIENT_ID},
        "referrer_uri": referrer_uri,
        "login_hint": login_hint,
    }
    return Response(
        {
            "url": furl(settings.IC_ACCOUNT_URL).add(query).url,
        }
    )


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def inclusion_connect_authenticate(request):
    code = request.data.get("code")
    state = request.data.get("state")
    frontend_state = request.data.get("frontend_state")
    stored_state = cache.get(f"oidc-state-{state}")
    if not (stored_state and (stored_state["state"] == state == frontend_state)):
        raise APIException("État oidc inconsistent")

    stored_nonce = stored_state["nonce"]
    stored_redirect_uri = stored_state["redirect_uri"]

    try:
        result = requests.post(
            url=settings.IC_TOKEN_URL,
            data={
                "client_id": settings.IC_CLIENT_ID,
                "client_secret": settings.IC_CLIENT_SECRET,
                "code": code,
                "grant_type": "authorization_code",
                "redirect_uri": stored_redirect_uri,
            },
        ).json()

        id_token = result["id_token"]
        decoded_id_token = jwt.decode(id_token, options={"verify_signature": False})
        code_safir = decoded_id_token.get("structure_pe")

        assert decoded_id_token["iss"] == settings.IC_ISSUER_ID
        assert settings.IC_CLIENT_ID in decoded_id_token["aud"]
        assert int(decoded_id_token["exp"]) > time.time()
        assert stored_nonce and stored_nonce == decoded_id_token["nonce"]

        user_dict = {
            "ic_id": decoded_id_token["sub"],
            "email": decoded_id_token["email"],
            "first_name": decoded_id_token["given_name"],
            "last_name": decoded_id_token["family_name"],
            "is_valid": True,
        }
        with transaction.atomic():
            try:
                # On essaye de récupérer un utilisateur déjà migré
                user, should_save = updated_ic_user(
                    User.objects.get(ic_id=user_dict["ic_id"]), user_dict["email"]
                )
                if user.first_name != user_dict["first_name"]:
                    user.first_name = user_dict["first_name"]
                    should_save = True
                if user.last_name != user_dict["last_name"]:
                    user.last_name = user_dict["last_name"]
                    should_save = True
                if user.is_valid != user_dict["is_valid"]:
                    user.is_valid = user_dict["is_valid"]
                    should_save = True
                if should_save:
                    user.save()
            except User.DoesNotExist:
                try:
                    # On essaye de faire la correspondance avec un utilisateur existant
                    # via son email, puis on le migre
                    user = User.objects.get(email=user_dict["email"])
                    if user.ic_id is not None:
                        logging.error("Conflit avec Keycloak")
                        return APIException("Conflit avec le fournisseur d'identité")
                    user.ic_id = user_dict["ic_id"]
                    user.first_name = user_dict["first_name"]
                    user.last_name = user_dict["last_name"]
                    user.is_valid = user_dict["is_valid"]
                    user.save()
                except User.DoesNotExist:
                    user = User.objects.create(**user_dict)

        update_last_login(user)
        try:
            token = Token.objects.get(user=user)
        except Token.DoesNotExist:
            token = Token.objects.create(user=user)
        return Response(
            {"token": token.key, "valid_user": True, "code_safir": code_safir}
        )
    except requests.exceptions.RequestException as e:
        logging.exception(e)
        raise APIException("Erreur de communication avec le fournisseur d'identité")


# Migration vers ProConnect :
# En parallèle des différents endpoints OIDC inclusion-connect (gardés pour problème éventuel).


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def oidc_login(request):
    # Simple redirection vers la page d'identification ProConnect (si pas identifié)
    return HttpResponseRedirect(
        redirect_to=reverse("oidc_authentication_init")
        + f"?{request.META.get("QUERY_STRING")}"
    )


@api_view(["GET"])
@permission_classes([permissions.AllowAny])
def oidc_logged_in(request):
    # étape indispensable pour le passage du token au frontend_state :
    # malheuresement, cette étape est "zappée" si un paramètre `next` est passé lors de l'identification
    # mozilla-django-oidc ne le prends pas en compte, il faut pour modifier la vue de callback et le redirect final

    # attention : l'utilisateur est toujours anonyme (a ce point il n'existe qu'un token DRF)
    token = Token.objects.get(user_id=request.session["_auth_user_id"])

    redirect_uri = f"{settings.FRONTEND_URL}/auth/pc-callback/{token}/"

    # gestion du next :
    if next := request.GET.get("next"):
        redirect_uri += f"?next={next}"

    # on redirige (pour l'instant) vers le front en faisant passer le token DRF
    return HttpResponseRedirect(redirect_to=redirect_uri)


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

    raise SuspiciousOperation("Tentative de déconnexion avec un token incorrect")


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

        success_url = resolve_url(self.get_settings("LOGIN_REDIRECT_URL", "/"))
        success_url += f"?{next_fieldname}={next_url}" if next_url else ""

        # redirection vers le front via `oidc/logged_in`
        return success_url


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
        else:
            raise SuspiciousOperation("Vérification de la déconnexion impossible")

        return super().post(request)
