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

    cookie = response.cookies["token_test"]
    assert cookie.value == token.key

    parsed_url = urlparse(response.url)
    query_params = parse_qs(parsed_url.query)
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
