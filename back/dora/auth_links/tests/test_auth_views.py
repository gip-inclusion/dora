from urllib.parse import parse_qs, urlparse

import pytest
import sesame.utils
from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.locmem import LocMemCache
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user
from dora.core.throttling import AuthLinkEmailThrottle, AuthLinkIpThrottle

# note : utilisation de `client` et pas `api_client`

# note : inutile de tester la durée de validité et l'usage unique,
# c'est de la response de `django-sesame`


@pytest.fixture(autouse=True)
def isolated_throttle_cache(monkeypatch):
    # Le cache par défaut (Redis) est partagé entre les tests et entre les exécutions
    throttle_cache = LocMemCache("auth-link-throttling-tests", {})
    # Les instances de même nom partagent leur contenu
    throttle_cache.clear()
    monkeypatch.setattr(AuthLinkIpThrottle, "cache", throttle_cache)
    monkeypatch.setattr(AuthLinkEmailThrottle, "cache", throttle_cache)


def test_send_link(client, mailoutbox):
    user_ic = make_user(is_active=True)

    response = client.post(
        reverse("send_link"),
        data={"email": user_ic.email},
    )
    assert response.status_code == 204, (
        "Une response 204 est attendue (utilisateur avec IC trouvé)"
    )
    assert len(mailoutbox) == 1
    assert mailoutbox[0].to == [user_ic.email]


def test_send_link_unknown_email(client, mailoutbox):
    response = client.post(reverse("send_link"), data={"email": "inconnu@example.com"})
    assert response.status_code == 204, (
        "La réponse ne doit pas révéler l'existence du compte"
    )
    assert mailoutbox == []


def test_send_link_is_throttled_per_ip(client, monkeypatch):
    monkeypatch.setattr(AuthLinkIpThrottle, "rate", "2/minute", raising=False)

    for i in range(2):
        response = client.post(
            reverse("send_link"), data={"email": f"inconnu-{i}@example.com"}
        )
        assert response.status_code == 204

    response = client.post(reverse("send_link"), data={"email": "autre@example.com"})
    assert response.status_code == 429


def test_send_link_is_throttled_per_email(client, monkeypatch):
    monkeypatch.setattr(AuthLinkEmailThrottle, "rate", "2/hour", raising=False)
    user = make_user(is_active=True)

    for i in range(2):
        response = client.post(
            reverse("send_link"),
            data={"email": user.email},
            REMOTE_ADDR=f"192.0.2.{i}",
        )
        assert response.status_code == 204

    # Même adresse, autre IP, casse différente
    response = client.post(
        reverse("send_link"),
        data={"email": user.email.upper()},
        REMOTE_ADDR="192.0.2.99",
    )
    assert response.status_code == 429


def test_authenticate_with_link(client):
    # Redirection vers l'accueil si le code fourni est invalide
    response = client.get(
        reverse("authenticate_with_link", kwargs={"sesame": "foo"}),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert response.url == settings.FRONTEND_URL, (
        "En cas d'échec, on doit rediriger vers l'accueil"
    )

    # Redirection vers l'identification du frontend si le code fourni est valide
    user = make_user(is_active=True)

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )
    assert response.status_code == 302, "Une redirection est attendue"
    assert "auth/callback" in response.url, (
        "On doit rediriger vers l'idetification du frontend"
    )
    assert "code=" in response.url, "L'URL doit contenir un code d'échange"


def test_authenticate_with_link_exchanges_code_for_token(client):
    """authenticate_with_link génère un code d'échange pointant vers le bon token."""
    user = make_user(is_active=True)
    token, _ = Token.objects.get_or_create(user=user)

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )

    assert response.status_code == 302
    assert "auth/callback" in response.url

    code = parse_qs(urlparse(response.url).query)["code"][0]
    assert cache.get(f"auth_code:{code}") == token.key


def test_authenticate_with_link_creates_token_if_not_exists(client):
    """authenticate_with_link crée un token s'il n'en existe pas."""
    user = make_user(is_active=True)

    assert not Token.objects.filter(user=user).exists()

    response = client.get(
        reverse(
            "authenticate_with_link", kwargs={"sesame": sesame.utils.get_token(user)}
        ),
    )

    assert response.status_code == 302
    assert Token.objects.filter(user=user).exists()

    token = Token.objects.get(user=user)

    code = parse_qs(urlparse(response.url).query)["code"][0]
    assert cache.get(f"auth_code:{code}") == token.key
