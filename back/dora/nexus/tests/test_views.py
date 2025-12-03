from unittest.mock import patch
from urllib.parse import urlencode

import pytest
from django.conf import settings
from django.urls import reverse
from rest_framework import status

from dora.core.test_utils import make_user
from dora.nexus.utils import generate_jwt


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
        with patch("dora.nexus.views.decode_jwt") as mock_decode:
            mock_decode.return_value = {}  # Pas d'email dans les claims
            response = api_client.post(
                reverse("auto-login-in"),
                data={"jwt": "some_token"},
                format="json",
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_user_not_authenticated_with_valid_jwt(self, api_client, user):
        """Test avec un utilisateur non authentifié et un token JWT valide"""
        token = generate_jwt(user)
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
        token = generate_jwt(user)
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
        token = generate_jwt(user)
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
        token = generate_jwt(user)
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
        token = generate_jwt(user)
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

    def test_decode_jwt_raises_value_error(self, api_client):
        """Test quand decode_jwt lève une ValueError"""
        with patch("dora.nexus.views.decode_jwt") as mock_decode:
            mock_decode.side_effect = ValueError("Invalid token")
            response = api_client.post(
                reverse("auto-login-in"),
                data={"jwt": "some_token"},
                format="json",
            )
            assert response.status_code == status.HTTP_204_NO_CONTENT
