from unittest.mock import patch

from django.conf import settings
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import make_service, make_structure, make_user
from dora.sirene.models import Establishment
from dora.structures.models import StructureMember
from dora.users.enums import DiscoveryMethod, MainActivity
from dora.users.models import User


class HandleEmploisOrientationTestCase(APITestCase):
    def setUp(self):
        self.service = make_service()
        self.structure = make_structure(siret="12345678901234")
        self.establishment = baker.make(Establishment, siret=self.structure.siret)
        self.user = make_user(email="prescriber@example.com")
        baker.make(StructureMember, structure=self.structure, user=self.user)

        self.valid_orientation_data = {
            "prescriber": {
                "email": self.user.email,
                "organization": {
                    "siret": self.structure.siret,
                },
            },
        }

        self.url = f"/orientations/emplois/{self.service.slug}/"

    def test_expired_token_redirects_to_login(self):
        with patch(
            "dora.orientations.views.decode_token", side_effect=ValueError("Expired")
        ):
            response = self.client.get(f"{self.url}?op=expired_token")

        assert response.status_code == 200
        assert response.data["toast_message"] == "Lien expiré"
        assert response.data["next_url"] == f"{settings.FRONTEND_URL}/auth/connexion"

    def test_authenticated_user_with_different_email_redirects_to_login(self):
        other_user = make_user(email="other@example.com")
        self.client.force_authenticate(user=other_user)

        with patch(
            "dora.orientations.views.decode_token",
            return_value=self.valid_orientation_data,
        ):
            response = self.client.get(f"{self.url}?op=valid_token")

        assert response.status_code == 200
        assert response.data["next_url"] == f"{settings.FRONTEND_URL}/auth/connexion"

    def test_creates_user_if_not_exists(self):
        new_email = "newuser@example.com"
        orientation_data = {
            "prescriber": {
                "email": new_email,
                "organization": {
                    "siret": self.structure.siret,
                },
            },
        }

        assert not User.objects.filter(email=new_email).exists()

        with patch(
            "dora.orientations.views.decode_token", return_value=orientation_data
        ):
            self.client.get(f"{self.url}?op=valid_token")

        user = User.objects.get(email=new_email)
        assert user.is_valid
        assert user.main_activity == MainActivity.ACCOMPAGNATEUR
        assert user.discovery_method == DiscoveryMethod.EMPLOIS_DE_L_INCLUSION

    def test_unknown_siret_returns_rattachement_url(self):
        unknown_siret = "99999999999999"
        orientation_data = {
            "prescriber": {
                "email": self.user.email,
                "organization": {
                    "siret": unknown_siret,
                },
            },
        }

        with patch(
            "dora.orientations.views.decode_token", return_value=orientation_data
        ):
            response = self.client.get(f"{self.url}?op=valid_token")

        assert response.status_code == 200
        assert response.data["known_siret"] is False
        assert (
            response.data["next_url"]
            == f"{settings.FRONTEND_URL}/auth/rattachement?siret={unknown_siret}"
        )

    def test_known_establishment_but_no_structure_returns_admin_flag_and_op_token(self):
        orphan_siret = "11111111111111"
        baker.make(Establishment, siret=orphan_siret)

        orientation_data = {
            "prescriber": {
                "email": self.user.email,
                "organization": {
                    "siret": orphan_siret,
                },
            },
        }

        with patch(
            "dora.orientations.views.decode_token", return_value=orientation_data
        ):
            response = self.client.get(f"{self.url}?op=valid_token")

        assert response.status_code == 200
        assert response.data["known_siret"] is False
        assert response.data["user_is_admin"] is True
        assert (
            response.data["next_url"]
            == f"{settings.FRONTEND_URL}/auth/rattachement?siret={orphan_siret}&op=valid_token"
        )

    def test_user_not_structure_member_returns_rattachement_with_token(self):
        non_member = make_user(email="nonmember@example.com")
        self.client.force_authenticate(user=non_member)

        orientation_data = {
            "prescriber": {
                "email": non_member.email,
                "organization": {
                    "siret": self.structure.siret,
                },
            },
        }

        with patch(
            "dora.orientations.views.decode_token", return_value=orientation_data
        ):
            response = self.client.get(f"{self.url}?op=valid_token")

        assert response.status_code == 200
        assert response.data["known_siret"] is True
        assert response.data["user_is_admin"] is False
        assert "op=valid_token" in response.data["next_url"]

    def test_valid_member_returns_service_url_with_orientation_token(self):
        self.client.force_authenticate(user=self.user)

        with patch(
            "dora.orientations.views.decode_token",
            return_value=self.valid_orientation_data,
        ):
            response = self.client.get(f"{self.url}?op=valid_token")

        assert response.status_code == 200
        assert response.data["user_structure_slug"] == self.structure.slug
        assert (
            response.data["next_url"]
            == f"{settings.FRONTEND_URL}/services/{self.service.slug}?orientation=valid_token"
        )
