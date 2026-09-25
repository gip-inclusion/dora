import uuid
from urllib.parse import parse_qs, urlparse

import pytest
from django.core.cache import cache
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user


def test_oidc_logged_in_exchanges_code_and_handles_next(client):
    """oidc_logged_in génère un code d'échange pointant vers le bon token et gère le paramètre next."""
    user = make_user()
    token, _ = Token.objects.get_or_create(user=user)

    session = client.session
    session["_auth_user_id"] = str(user.id)
    session.save()

    next_url = "/some/path"
    response = client.get(reverse("oidc_logged_in"), {"next": next_url})

    assert response.status_code == 302

    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)

    assert "auth/callback" in response.url
    code = query_params["code"][0]
    assert cache.get(f"auth_code:{code}") == token.key

    assert query_params["next"][0] == next_url


@pytest.mark.parametrize(
    "url_name",
    [
        "oidc_authentication_init",
    ],
)
def test_oidc_authentication_views_have_no_cache_headers(client, url_name):
    """Les vues d'authentification OIDC ne doivent pas être mises en cache.

    C'est essentiel pour éviter que les redirections 302 (contenant state,
    nonce et login_hint) ne soient mises en cache par un CDN ou proxy.
    """
    response = client.get(reverse(url_name))

    cache_control = response.get("Cache-Control", "")
    assert "no-store" in cache_control or "no-cache" in cache_control


def test_oidc_login_creates_drf_token_with_existing_session(client, mocker):
    # Avec une session Django déjà ouverte (ici via l'admin), `mozilla-django-oidc`
    # ne rappelle pas `auth.login()` : le token doit être créé à l'authentification.
    user = make_user(sub_pc=uuid.uuid4())
    client.force_login(user, backend="django.contrib.auth.backends.ModelBackend")
    backend = "dora.oidc.backends.OIDCAuthenticationBackend"
    mocker.patch(f"{backend}.get_token", return_value={})
    mocker.patch(f"{backend}.verify_token", return_value={"sub": str(user.sub_pc)})
    mocker.patch(
        f"{backend}.get_userinfo",
        return_value={"email": user.email, "sub": str(user.sub_pc)},
    )
    session = client.session
    session["oidc_states"] = {"a-state": {"nonce": "a-nonce", "code_verifier": None}}
    session.save()

    client.get(
        reverse("oidc_authentication_callback"), {"code": "a-code", "state": "a-state"}
    )
    response = client.get(reverse("oidc_logged_in"))

    assert response.status_code == 302
    assert Token.objects.filter(user=user).exists()
