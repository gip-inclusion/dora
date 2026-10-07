from unittest.mock import patch
from urllib.parse import parse_qs, urlencode, urlparse

import pytest
from django.conf import settings
from django.urls import reverse
from itoutils.django.nexus.token import decode_token, generate_auto_login_token
from rest_framework import status

from dora.core.test_utils import make_user


@pytest.fixture
def user():
    return make_user(email="test@example.com")


@pytest.fixture
def other_user():
    return make_user(email="other@example.com")


class TestAutoLoginIn:
    def test_invalid_jwt_token(self, api_client):
        """Test avec un token JWT invalide"""
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": "invalid_token"},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_missing_jwt_token(self, api_client):
        """Test sans token JWT"""
        response = api_client.post(
            reverse("auto-login-in"),
            data={},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_jwt_without_email(self, api_client, user):
        """Test avec un token JWT valide mais sans email dans les claims"""
        with patch("itoutils.django.nexus.token.decode_token") as mock_decode:
            mock_decode.return_value = {}  # Pas d'email dans les claims
            response = api_client.post(
                reverse("auto-login-in"),
                data={"jwt": "some_token"},
                format="json",
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_not_authenticated_with_valid_jwt(self, api_client, user):
        """Test avec un utilisateur non authentifié et un token JWT valide"""
        token = generate_auto_login_token(user)
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": token},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

        params = {"login_hint": user.email}
        authorize_url = reverse("oidc_authentication_init")
        authorize_url += "?" + urlencode(params)
        expected_url = response.wsgi_request.build_absolute_uri(authorize_url)

        assert response.data["redirect_url"] == expected_url

    def test_user_not_authenticated_with_valid_jwt_and_next_url(self, api_client, user):
        """Test avec un utilisateur non authentifié, un token valide et un next_url"""
        token = generate_auto_login_token(user)
        next_url = "/some/path"
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": token, "next": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

        params = {"next": next_url, "login_hint": user.email}
        authorize_url = reverse("oidc_authentication_init")
        authorize_url += "?" + urlencode(params)
        expected_url = response.wsgi_request.build_absolute_uri(authorize_url)

        assert response.data["redirect_url"] == expected_url

    def test_user_already_authenticated_same_email(self, api_client, user):
        """Test avec un utilisateur déjà authentifié avec le même email"""
        token = generate_auto_login_token(user)
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": token},
            format="json",
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_already_authenticated_different_email(
        self, api_client, user, other_user
    ):
        """Test avec un utilisateur déjà authentifié avec un email différent"""
        token = generate_auto_login_token(user)
        api_client.force_authenticate(user=other_user)
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": token},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

        expected_url = f"{settings.FRONTEND_URL}/auth/pc-logout/"
        assert response.data["redirect_url"] == expected_url

    def test_user_already_authenticated_different_email_with_next_url(
        self, api_client, user, other_user
    ):
        """Test avec un utilisateur déjà authentifié avec un email différent et un next_url"""
        token = generate_auto_login_token(user)
        api_client.force_authenticate(user=other_user)
        next_url = "/some/path"
        response = api_client.post(
            reverse("auto-login-in"),
            data={"jwt": token, "next": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK

        expected_url = f"{settings.FRONTEND_URL}/auth/pc-logout/"
        assert response.data["redirect_url"] == expected_url

    def test_decode_token_raises_value_error(self, api_client):
        """Test quand decode_token lève une ValueError"""
        with patch("itoutils.django.nexus.token.decode_token") as mock_decode:
            mock_decode.side_effect = ValueError("Invalid token")
            response = api_client.post(
                reverse("auto-login-in"),
                data={"jwt": "some_token"},
                format="json",
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT


class TestAutoLoginOut:
    def test_user_not_authenticated(self, api_client):
        """Test avec un utilisateur non authentifié"""
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next": "https://domain.fr/some/path"},
            format="json",
        )
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_user_authenticated_without_next_param(self, api_client, user):
        """Test avec un utilisateur authentifié mais sans paramètre next_url"""
        api_client.force_authenticate(user=user)
        response = api_client.post(
            reverse("auto-login-out"),
            data={},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_authenticated_with_next_url_but_no_key(self, api_client, user):
        """Test avec un utilisateur authentifié avec next_url mais PDI_JWT_KEY est None"""
        api_client.force_authenticate(user=user)
        with patch.object(settings, "PDI_JWT_KEY", None):
            response = api_client.post(
                reverse("auto-login-out"),
                data={"next_url": "https://domain.fr/some/path"},
                format="json",
            )
            assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_authenticated_with_valid_next_url(self, api_client, user):
        """Test avec un utilisateur authentifié et une URL next_url valide et autorisée"""
        api_client.force_authenticate(user=user)
        next_url = "https://domain.fr/some/path"
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next_url": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "redirect_url" in response.data
        redirect_url = response.data["redirect_url"]
        assert redirect_url.startswith(next_url)

        # Vérifier que le paramètre auto_login est présent dans l'URL
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        assert "auto_login" in query_params

        # Vérifier que le token JWT est valide
        auto_login_token = query_params["auto_login"][0]
        claims = decode_token(auto_login_token)
        assert claims["email"] == user.email

    def test_user_authenticated_with_next_url_and_existing_params(
        self, api_client, user
    ):
        """Test avec une URL next qui contient déjà des paramètres"""
        api_client.force_authenticate(user=user)
        next_url = "https://domain.fr/some/path?existing=param"
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next_url": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "redirect_url" in response.data
        redirect_url = response.data["redirect_url"]
        assert redirect_url.startswith("https://domain.fr/some/path")

        # Vérifier que les paramètres existants sont préservés
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        assert "existing" in query_params
        assert query_params["existing"][0] == "param"
        assert "auto_login" in query_params

    def test_user_authenticated_with_unauthorized_host(self, api_client, user):
        """Test avec un utilisateur authentifié mais un host non autorisé"""
        api_client.force_authenticate(user=user)
        next_url = "https://evil.com/some/path"
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next_url": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_authenticated_with_http_instead_of_https(self, api_client, user):
        """Test avec un utilisateur authentifié mais une URL HTTP au lieu de HTTPS"""
        api_client.force_authenticate(user=user)
        next_url = "http://domain.fr/some/path"
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next_url": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_user_authenticated_with_valid_next_url_different_domain(
        self, api_client, user
    ):
        """Test avec un utilisateur authentifié et une URL next valide sur un autre domaine autorisé"""
        api_client.force_authenticate(user=user)
        next_url = "https://domain.com/another/path"
        response = api_client.post(
            reverse("auto-login-out"),
            data={"next_url": next_url},
            format="json",
        )
        assert response.status_code == status.HTTP_200_OK
        assert "redirect_url" in response.data
        redirect_url = response.data["redirect_url"]
        assert redirect_url.startswith(next_url)

        # Vérifier que le paramètre auto_login est présent
        parsed_url = urlparse(redirect_url)
        query_params = parse_qs(parsed_url.query)
        assert "auto_login" in query_params

        # Vérifier que le token JWT est valide
        auto_login_token = query_params["auto_login"][0]
        claims = decode_token(auto_login_token)
        assert claims["email"] == user.email
