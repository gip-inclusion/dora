from unittest.mock import MagicMock
from urllib.parse import parse_qs, urlparse

import pytest
from django.urls import reverse
from rest_framework.authtoken.models import Token

from dora.core.test_utils import make_user
from dora.oidc.views import CustomAuthorizationCallbackView


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


class TestCustomAuthorizationCallbackView:
    def _make_view(self, next_url):
        """Instancie la vue avec une session contenant oidc_login_next."""
        view = CustomAuthorizationCallbackView()
        view.request = MagicMock()
        view.request.session = {"oidc_login_next": next_url}
        return view

    def test_success_url_preserves_all_query_params_in_next(self):
        """
        Régression : le next_url contenant plusieurs paramètres de requête
        (ex: &op=TOKEN&mtm_kwd=...) doit être entièrement encodé dans le
        paramètre `next` de l'URL de redirection.

        Sans encodage, les `&` du next_url sont interprétés comme des séparateurs
        de paramètres de premier niveau, ce qui fait perdre `op` (et les autres
        paramètres) lors du parsing dans oidc_logged_in.
        """
        next_url = "https://staging.dora.inclusion.gouv.fr/services/my-service?mtm_campaign=lesemplois&mtm_kwd=rechservice-prescriber&op=TOKEN123"

        success_url = self._make_view(next_url).success_url

        parsed = urlparse(success_url)
        query_params = parse_qs(parsed.query)

        assert "next" in query_params
        assert query_params["next"][0] == next_url
