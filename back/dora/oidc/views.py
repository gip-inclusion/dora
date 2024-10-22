import logging
import time

import jwt
import requests
from django.conf import settings
from django.core.cache import cache
from django.db import transaction
from django.utils.crypto import get_random_string
from furl import furl
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
