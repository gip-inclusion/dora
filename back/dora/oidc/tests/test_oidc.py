import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user


@pytest.fixture
def user_with_token():
    user = make_user()
    Token.objects.create(user=user)
    return user


class TestOidcLoggedIn:
    def test_redirects_with_valid_next_url(self, client, user_with_token):
        session = client.session
        session["_auth_user_id"] = str(user_with_token.pk)
        session.save()

        response = client.get(
            reverse("oidc_logged_in"),
            {"next": "http://localhost:3000/services/test-service?foo=bar"},
        )

        assert response.status_code == 302
        assert "next=%2Fservices%2Ftest-service%3Ffoo%3Dbar" in response.url

    def test_handles_malformed_ipv6_url_gracefully(self, client, user_with_token):
        session = client.session
        session["_auth_user_id"] = str(user_with_token.pk)
        session.save()

        # URL avec IPv6 malformée qui ferait planter urlparse
        response = client.get(
            reverse("oidc_logged_in"),
            {"next": "https://[::1/"},
        )

        # Ne doit pas lever d'exception, redirige sans le paramètre next
        assert response.status_code == 302
        assert "next=" not in response.url

    def test_redirects_without_next_param(self, client, user_with_token):
        session = client.session
        session["_auth_user_id"] = str(user_with_token.pk)
        session.save()

        response = client.get(reverse("oidc_logged_in"))

        assert response.status_code == 302
        assert "next=" not in response.url
