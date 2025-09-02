from unittest import TestCase
from unittest.mock import Mock, patch

from django.test import override_settings
from model_bakery import baker

from dora.core.test_utils import make_structure, make_user
from dora.onboarding import _setup_brevo_client as original_setup_brevo_client
from dora.onboarding import onboard_user
from dora.structures.models import StructureMember, StructurePutativeMember
from dora.users.enums import MainActivity


@patch("dora.onboarding._create_or_update_brevo_contact")
@patch("dora.onboarding._contact_in_brevo_list")
@patch("dora.onboarding._remove_from_brevo_list")
@patch("dora.onboarding._setup_brevo_client")
class OnboardUserTestCase(TestCase):
    def setUp(self):
        self.settings_patcher = override_settings(
            BREVO_ACTIVE=True,
            BREVO_API_KEY="test_api_key",
            BREVO_ONBOARDING_MEMBER_LIST=123,
            BREVO_ONBOARDING_PUTATIVE_MEMBER_LIST=456,
        )
        self.settings_patcher.enable()

        self.user = make_user(
            email="test@example.com",
            first_name="John",
            last_name="Doe",
            main_activity="activity_test",
        )
        self.structure = make_structure(
            name="Test Structure", city_code="75001", department="75"
        )

    def tearDown(self):
        self.settings_patcher.disable()

    def test_add_all_users_to_same_onboarding_list_regardless_of_main_activity(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client

        main_activities = [
            MainActivity.ACCOMPAGNATEUR,
            MainActivity.OFFREUR,
            MainActivity.ACCOMPAGNATEUR_OFFREUR,
            MainActivity.AUTRE,
        ]

        for i, main_activity in enumerate(main_activities):
            with self.subTest(variation=i):
                user = make_user(main_activity=main_activity)
                baker.make(StructureMember, user=user, structure=self.structure)

                mock_create_or_update.reset_mock()

                onboard_user(user, self.structure)

                onboarding_list = mock_create_or_update.call_args[0][3]
                self.assertEqual(onboarding_list, 123)

    @override_settings(BREVO_ACTIVE=False)
    @override_settings(ENVIRONMENT="TEST")
    @patch("dora.onboarding.logger.warning")
    def test_onboard_user_brevo_inactive_returns_early(
        self,
        mock_logger,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_setup_client.side_effect = original_setup_brevo_client
        onboard_user(self.user, self.structure)

        mock_logger.assert_called_once_with(
            "L'API Brevo n'est pas active sur cet environnement TEST"
        )

    def test_onboard_user_new_member_creates_contact_in_member_list(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = False

        baker.make(
            StructureMember, user=self.user, structure=self.structure, is_admin=True
        )

        onboard_user(self.user, self.structure)

        expected_attributes = {
            "PRENOM": "John",
            "NOM": "Doe",
            "PROFIL": "activity_test",
            "IS_ADMIN": True,
            "IS_FIRST_ADMIN": False,
            "URL_DORA_STRUCTURE": self.structure.get_frontend_url(),
            "NEED_VALIDATION": False,
            "NOM_STRUCTURE": self.structure.name,
            "CONTACT_ADHESION": [self.user.email],
            "VILLE": self.structure.city,
            "CITY_CODE_DORA": self.structure.city_code,
            "NO_DEPARTEMENT": self.structure.department,
        }

        mock_create_or_update.assert_called_once_with(
            mock_client, self.user, expected_attributes, 123
        )
        mock_remove_from_list.assert_not_called()

    def test_onboard_user_putative_member_creates_contact_in_putative_list(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = False

        baker.make(
            StructurePutativeMember,
            user=self.user,
            structure=self.structure,
            is_admin=False,
        )

        onboard_user(self.user, self.structure)

        expected_attributes = {
            "PRENOM": "John",
            "NOM": "Doe",
            "PROFIL": "activity_test",
            "IS_ADMIN": False,
            "IS_FIRST_ADMIN": True,
            "URL_DORA_STRUCTURE": self.structure.get_frontend_url(),
            "NEED_VALIDATION": True,
            "NOM_STRUCTURE": "Test Structure",
            "CONTACT_ADHESION": [],
            "VILLE": self.structure.city,
            "CITY_CODE_DORA": "75001",
            "NO_DEPARTEMENT": "75",
        }

        mock_create_or_update.assert_called_once_with(
            mock_client, self.user, expected_attributes, 456
        )
        mock_remove_from_list.assert_not_called()

    def test_onboard_user_member_removed_from_putative_list_if_present(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = True

        baker.make(
            StructureMember, user=self.user, structure=self.structure, is_admin=False
        )

        onboard_user(self.user, self.structure)

        mock_contact_in_list.assert_called_once_with(mock_client, self.user, 456)
        mock_remove_from_list.assert_called_once_with(mock_client, self.user, 456)

    def test_onboard_user_member_not_removed_from_putative_list_if_not_present(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = False

        baker.make(
            StructureMember, user=self.user, structure=self.structure, is_admin=False
        )

        onboard_user(self.user, self.structure)

        mock_contact_in_list.assert_called_once_with(mock_client, self.user, 456)
        mock_remove_from_list.assert_not_called()

    def test_onboard_user_with_existing_admin_sets_first_admin_false(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = False

        baker.make(
            StructureMember,
            user=make_user(email="admin@example.com"),
            structure=self.structure,
            is_admin=True,
        )
        baker.make(
            StructureMember, user=self.user, structure=self.structure, is_admin=False
        )

        onboard_user(self.user, self.structure)

        call_args = mock_create_or_update.call_args[0]
        attributes = call_args[2]

        self.assertFalse(attributes["IS_FIRST_ADMIN"])
        self.assertFalse(attributes["IS_ADMIN"])
        self.assertEqual(attributes["CONTACT_ADHESION"], ["admin@example.com"])

    def test_onboard_user_with_multiple_admins_includes_all_admin_emails(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_client = Mock()
        mock_setup_client.return_value = mock_client
        mock_contact_in_list.return_value = False

        baker.make(
            StructureMember,
            user=make_user(email="admin2@example.com"),
            structure=self.structure,
            is_admin=True,
        )
        baker.make(
            StructureMember,
            user=make_user(email="admin1@example.com"),
            structure=self.structure,
            is_admin=True,
        )
        baker.make(
            StructureMember, user=self.user, structure=self.structure, is_admin=False
        )

        onboard_user(self.user, self.structure)

        call_args = mock_create_or_update.call_args[0]
        attributes = call_args[2]

        admin_emails = attributes["CONTACT_ADHESION"]
        self.assertIn("admin1@example.com", admin_emails)
        self.assertIn("admin2@example.com", admin_emails)
        self.assertEqual(len(admin_emails), 2)

    def test_onboard_user_setup_client_returns_none_skips_processing(
        self,
        mock_setup_client,
        mock_remove_from_list,
        mock_contact_in_list,
        mock_create_or_update,
    ):
        mock_setup_client.return_value = None

        result = onboard_user(self.user, self.structure)

        self.assertIsNone(result)
