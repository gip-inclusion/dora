import csv
from io import StringIO
from unittest.mock import patch

from django.test import TestCase
from model_bakery import baker

from dora.core.csv_user_import import ImportUserHelper
from dora.core.test_utils import make_structure
from dora.structures.models import StructureMember, StructurePutativeMember
from dora.users.models import User


@patch("dora.core.csv_user_import.send_invitation_email")
class ImportUserHelperTestCase(TestCase):
    def setUp(self):
        self.helper = ImportUserHelper()
        self.structure = make_structure(siret="12345678901234")
        self.csv_headers = "structure_siret,email,prenom,nom\n"

    def test_import_users_wet_run_creates_new_user_and_invitation(
        self, mock_send_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.assertFalse(User.objects.filter(email="john.doe@example.com").exists())
        self.assertEqual(StructurePutativeMember.objects.count(), 0)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        user = User.objects.get(email="john.doe@example.com")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

        putative_member = StructurePutativeMember.objects.get(
            user=user, structure=self.structure
        )
        self.assertTrue(putative_member.is_admin)
        self.assertTrue(putative_member.invited_by_admin)

        mock_send_invitation_email.assert_called_once_with(
            putative_member, "L’équipe DORA"
        )

    def test_import_users_dry_run_no_db_changes(self, mock_send_invitation_email):
        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=False, make_users_admin=True)

        self.assertFalse(User.objects.filter(email="john.doe@example.com").exists())
        self.assertEqual(StructurePutativeMember.objects.count(), 0)
        mock_send_invitation_email.assert_not_called()

    def test_import_users_existing_user_does_not_send_email(
        self, mock_send_invitation_email
    ):
        existing_user = baker.make(
            User, email="john.doe@example.com", first_name="John", last_name="Doe"
        )

        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=False)

        self.assertEqual(User.objects.filter(email="john.doe@example.com").count(), 1)

        putative_member = StructurePutativeMember.objects.get(
            user=existing_user, structure=self.structure
        )
        self.assertFalse(putative_member.is_admin)
        self.assertTrue(putative_member.invited_by_admin)

        mock_send_invitation_email.assert_called_once_with(
            putative_member, "L’équipe DORA"
        )

    def test_import_users_existing_putative_member_upgrades_admin(
        self, mock_send_invitation_email
    ):
        user = baker.make(User, email="john.doe@example.com")
        existing_putative_member = baker.make(
            StructurePutativeMember, user=user, structure=self.structure, is_admin=False
        )

        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        existing_putative_member.refresh_from_db()
        self.assertTrue(existing_putative_member.is_admin)
        mock_send_invitation_email.assert_not_called()

    def test_import_users_existing_member_upgrades_admin(
        self, mock_send_invitation_email
    ):
        user = baker.make(User, email="john.doe@example.com")
        existing_member = baker.make(
            StructureMember, user=user, structure=self.structure, is_admin=False
        )

        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        existing_member.refresh_from_db()
        self.assertTrue(existing_member.is_admin)
        mock_send_invitation_email.assert_not_called()

    def test_import_users_invalid_structure_siret_not_imported(
        self, mock_send_invitation_email
    ):
        csv_content = f"{self.csv_headers}invalid_siret,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertFalse(User.objects.filter(email="john.doe@example.com").exists())
        self.assertEqual(StructurePutativeMember.objects.count(), 0)

    def test_import_users_multiple_rows_processes_all(self, mock_send_invitation_email):
        structure2 = make_structure(siret="98765432109876")

        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe\n98765432109876,jane.smith@example.com,Jane,Smith"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        user1 = User.objects.get(email="john.doe@example.com")
        user2 = User.objects.get(email="jane.smith@example.com")

        putative_member1 = StructurePutativeMember.objects.get(
            user=user1, structure=self.structure
        )
        putative_member2 = StructurePutativeMember.objects.get(
            user=user2, structure=structure2
        )

        self.assertTrue(putative_member1.is_admin)
        self.assertTrue(putative_member2.is_admin)
        self.assertEqual(mock_send_invitation_email.call_count, 2)

    def test_import_users_one_error_nothing_saved(self, mock_send_invitation_email):
        csv_content = f"{self.csv_headers}12345678901234,new1@example.com,John,Doe\ninvalid,new2@example.com,Jane,Smith"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertFalse(User.objects.filter(email="new1@example.com").exists())
        self.assertFalse(User.objects.filter(email="new2@example.com").exists())

        self.assertEqual(mock_send_invitation_email.call_count, 0)

    def test_import_users_with_spaces_in_names_processes_correctly(
        self, mock_send_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345678901234,jean.pierre@example.com,Jean Pierre,Van Der Berg"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        user = User.objects.get(email="jean.pierre@example.com")
        self.assertEqual(user.first_name, "Jean Pierre")
        self.assertEqual(user.last_name, "Van Der Berg")

        putative_member = StructurePutativeMember.objects.get(
            user=user, structure=self.structure
        )
        self.assertTrue(putative_member.is_admin)
        mock_send_invitation_email.assert_called_once()

    def test_import_users_with_missing_email_not_imported(
        self, mock_send_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345678901234,,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertFalse(
            User.objects.filter(first_name="John", last_name="Doe").exists(), 0
        )
        mock_send_invitation_email.assert_not_called()

    def test_import_users_with_missing_names_creates_user_with_empty_names(
        self, mock_send_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,,"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        user = User.objects.get(email="john.doe@example.com")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_missing_headers(self, mock_send_invitation_email):
        csv_content = (
            "invalid,email,prenom,nom\n12345678901234,john.doe@example.com,John,Doe"
        )
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertFalse(User.objects.filter(email="john.doe@example.com").exists())
        mock_send_invitation_email.assert_not_called()

    def test_idempotence(self, mock_send_invitation_email):
        csv_content = f"{self.csv_headers}12345678901234,john.doe@example.com,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)
        initial_user_count = User.objects.count()
        initial_putative_member_count = StructurePutativeMember.objects.count()

        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)
        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertEqual(User.objects.count(), initial_user_count)
        self.assertEqual(
            StructurePutativeMember.objects.count(), initial_putative_member_count
        )
        self.assertEqual(mock_send_invitation_email.call_count, 1)


@patch("dora.core.csv_user_import.send_france_travail_invitation_email")
class ImportFranceTravailUsersTestCase(TestCase):
    def setUp(self):
        self.helper = ImportUserHelper()
        self.structure = make_structure(siret="12345678901234")
        self.france_travail_structure = make_structure(code_safir_ft="12345")
        self.csv_headers = "safir,email,prenom,nom\n"

    def test_import_france_travail_users_wet_run_creates_new_user_and_invitation(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,john.doe@francetravail.fr,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.assertFalse(
            User.objects.filter(email="john.doe@francetravail.fr").exists()
        )
        self.assertEqual(StructurePutativeMember.objects.count(), 0)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        user = User.objects.get(email="john.doe@francetravail.fr")
        self.assertEqual(user.first_name, "John")
        self.assertEqual(user.last_name, "Doe")

        putative_member = StructurePutativeMember.objects.get(
            user=user, structure=self.france_travail_structure
        )
        self.assertTrue(putative_member.is_admin)
        self.assertTrue(putative_member.invited_by_admin)

        mock_send_france_travail_invitation_email.assert_called_once_with(
            putative_member, "L’équipe DORA"
        )

    def test_import_france_travail_users_dry_run_no_db_changes(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,john.doe@francetravail.fr,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=False, make_users_admin=True
        )

        self.assertFalse(
            User.objects.filter(email="john.doe@francetravail.fr").exists()
        )
        self.assertEqual(StructurePutativeMember.objects.count(), 0)
        mock_send_france_travail_invitation_email.assert_not_called()

    def test_import_france_travail_users_generates_email_when_missing(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,Jean-Pierre,Dupont"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        expected_email = "jean-pierre.dupont@francetravail.fr"
        user = User.objects.get(email=expected_email)
        self.assertEqual(user.first_name, "Jean-Pierre")
        self.assertEqual(user.last_name, "Dupont")

        putative_member = StructurePutativeMember.objects.get(
            user=user, structure=self.france_travail_structure
        )
        self.assertTrue(putative_member.is_admin)

        mock_send_france_travail_invitation_email.assert_called_once_with(
            putative_member, "L’équipe DORA"
        )

    def test_import_france_travail_users_strips_accents_in_generated_email(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,François,Müller"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        expected_email = "francois.muller@francetravail.fr"
        user = User.objects.get(email=expected_email)
        self.assertEqual(user.first_name, "François")
        self.assertEqual(user.last_name, "Müller")

    def test_import_france_travail_users_existing_putative_member_upgrades_admin(
        self, mock_send_france_travail_invitation_email
    ):
        user = baker.make(User, email="john.doe@francetravail.fr")
        existing_putative_member = baker.make(
            StructurePutativeMember,
            user=user,
            structure=self.france_travail_structure,
            is_admin=False,
        )

        csv_content = f"{self.csv_headers}12345,john.doe@francetravail.fr,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        existing_putative_member.refresh_from_db()
        self.assertTrue(existing_putative_member.is_admin)
        mock_send_france_travail_invitation_email.assert_not_called()

    def test_import_france_travail_users_invalid_safir_not_imported(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = (
            f"{self.csv_headers}invalid_safir,john.doe@francetravail.fr,John,Doe"
        )
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        self.assertFalse(
            User.objects.filter(email="john.doe@francetravail.fr").exists()
        )
        self.assertEqual(StructurePutativeMember.objects.count(), 0)

    def test_import_france_travail_users_multiple_rows_processes_all(
        self, mock_send_france_travail_invitation_email
    ):
        structure2 = make_structure(code_safir_ft="67890")

        csv_content = f"{self.csv_headers}12345,john.doe@francetravail.fr,John,Doe\n67890,jane.smith@francetravail.fr,Jane,Smith"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        user1 = User.objects.get(email="john.doe@francetravail.fr")
        user2 = User.objects.get(email="jane.smith@francetravail.fr")

        putative_member1 = StructurePutativeMember.objects.get(
            user=user1, structure=self.france_travail_structure
        )
        putative_member2 = StructurePutativeMember.objects.get(
            user=user2, structure=structure2
        )

        self.assertTrue(putative_member1.is_admin)
        self.assertTrue(putative_member2.is_admin)
        self.assertEqual(mock_send_france_travail_invitation_email.call_count, 2)

    def test_import_france_travail_users_one_error_nothing_saved(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,new1@francetravail.fr,John,Doe\ninvalid,new2@francetravail.fr,Jane,Smith"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        self.assertFalse(User.objects.filter(email="new1@francetravail.fr").exists())
        self.assertFalse(User.objects.filter(email="new2@francetravail.fr").exists())

        self.assertEqual(mock_send_france_travail_invitation_email.call_count, 0)

    def test_import_france_travail_users_with_spaces_in_names_processes_correctly(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,jean.pierre@francetravail.fr,Jean Pierre,Van Der Berg"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        user = User.objects.get(email="jean.pierre@francetravail.fr")
        self.assertEqual(user.first_name, "Jean Pierre")
        self.assertEqual(user.last_name, "Van Der Berg")

        putative_member = StructurePutativeMember.objects.get(
            user=user, structure=self.france_travail_structure
        )
        self.assertTrue(putative_member.is_admin)
        mock_send_france_travail_invitation_email.assert_called_once()

    def test_import_france_travail_users_with_missing_names_not_imported(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,,"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        mock_send_france_travail_invitation_email.assert_not_called()
        self.assertEqual(StructurePutativeMember.objects.count(), 0)

    def test_import_france_travail_users_with_only_first_name_not_imported(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,John,"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        self.assertFalse(User.objects.filter(first_name="John").exists())
        self.assertEqual(StructurePutativeMember.objects.count(), 0)
        mock_send_france_travail_invitation_email.assert_not_called()

    def test_import_france_travail_users_with_only_last_name_not_imported(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        self.assertFalse(User.objects.filter(last_name="Doe").exists())
        self.assertEqual(StructurePutativeMember.objects.count(), 0)
        mock_send_france_travail_invitation_email.assert_not_called()

    def test_import_france_travail_users_with_spaces_in_names_generates_correct_email(
        self, mock_send_france_travail_invitation_email
    ):
        csv_content = f"{self.csv_headers}12345,,Jean Pierre,Van Der Berg"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        expected_email = "jean-pierre.van-der-berg@francetravail.fr"
        user = User.objects.get(email=expected_email)
        self.assertEqual(user.first_name, "Jean Pierre")
        self.assertEqual(user.last_name, "Van Der Berg")

    def test_missing_headers(self, mock_send_france_travail_invitation_email):
        csv_content = (
            "invalid,email,prenom,nom\n12345,john.doe@francetravail.fr,John,Doe"
        )
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_users(reader, wet_run=True, make_users_admin=True)

        self.assertFalse(User.objects.filter(email="john.doe@francetravailfr").exists())
        mock_send_france_travail_invitation_email.assert_not_called()

    def test_idempotence(self, mock_send_france_travail_invitation_email):
        csv_content = f"{self.csv_headers}12345,john.doe@francetravail.fr,John,Doe"
        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)

        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )
        initial_user_count = User.objects.count()
        initial_putative_member_count = StructurePutativeMember.objects.count()

        csv_file = StringIO(csv_content)
        reader = csv.reader(csv_file)
        self.helper.import_france_travail_users(
            reader, wet_run=True, make_users_admin=True
        )

        self.assertEqual(User.objects.count(), initial_user_count)
        self.assertEqual(
            StructurePutativeMember.objects.count(), initial_putative_member_count
        )
        self.assertEqual(mock_send_france_travail_invitation_email.call_count, 1)
