from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user


def test_oidc_logged_in_sets_cookie_and_handles_next(client):
    """oidc_logged_in définit le cookie d'authentification et gère le paramètre next."""
    user = make_user()
    token, _ = Token.objects.get_or_create(user=user)

    session = client.session
    session["_auth_user_id"] = str(user.id)
    session.save()

    next_url = "/some/path"
    response = client.get(reverse("oidc_logged_in"), {"next": next_url})

    assert response.status_code == 302
    assert "token" in response.cookies

    cookie = response.cookies["token"]
    assert cookie.value == token.key
    assert cookie["path"] == "/"
    assert cookie["samesite"] == "Lax"
    assert cookie["secure"] is True
    assert cookie.get("httponly", "") != "HttpOnly"

    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)
    assert "next" in query_params
    assert query_params["next"][0] == next_url
