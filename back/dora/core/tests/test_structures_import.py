import csv
import tempfile
from io import StringIO
from urllib.parse import quote

from django.core import mail
from django.core.management import call_command
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import make_model, make_service, make_structure, make_user
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
    StructureSource,
)
from dora.users.models import User


class StructuresImportTestCase(APITestCase):
    def setUp(self):
        self.tmp_file = tempfile.NamedTemporaryFile(mode="w", newline="")
        self.csv_writer = self.create_csv(self.tmp_file)

    def create_csv(self, file):
        writer = csv.writer(file, delimiter=",")
        writer.writerow(
            [
                "nom",
                "siret",
                "siret_parent",
                "courriels_administrateurs",
                "labels",
                "modeles",
                "telephone",
                "courriel_structure",
            ]
        )
        return writer

    def add_row(self, row):
        self.csv_writer.writerow(row)

    def call_command(self):
        self.tmp_file.seek(0)
        out = StringIO()
        err = StringIO()
        call_command(
            "import_structures",
            self.tmp_file.name,
            stdout=out,
            stderr=err,
            wet_run=True,
        )
        self.tmp_file.seek(0)
        return out.getvalue(), err.getvalue()

    ########

    # Validité des sirets
    def test_unknown_siret_wont_create_anything(self):
        self.add_row(["foo", "12345678901234", "", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("Siret inconnu", err)
        self.assertFalse(Structure.objects.filter(siret="12345678901234").exists())
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_siret_wont_create_anything(self):
        self.add_row(["foo", "1234", "", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("Le numéro SIRET doit être composé de 14 chiffres.", err)
        self.assertIn("siret", err)
        self.assertFalse(Structure.objects.filter(siret="12345").exists())
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_parent_siret_error(self):
        self.add_row(["foo", "", "1234", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("Le numéro SIRET doit être composé de 14 chiffres.", err)
        self.assertIn("parent_siret", err)

    def test_unknown_parent_siret_error(self):
        self.add_row(["foo", "", "12345678901234", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("SIRET parent inconnu", err)

    def test_missing_siret_error(self):
        self.add_row(["foo", "", "", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("`siret` ou `parent_siret` sont requis", err)

    def test_no_recursive_branch(self):
        parent = make_structure()
        make_structure(parent=parent, siret="12345678901234")
        self.add_row(["foo", "", "12345678901234", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn(
            "Le SIRET 12345678901234 est une antenne, il ne peut pas être utilisé comme parent",
            err,
        )

    #
    def test_can_invite_new_user(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        user = User.objects.filter(email="foo@buzz.com").first()
        self.assertIsNotNone(user)
        self.assertEqual(user.get_full_name(), "foo@buzz.com")
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[DORA] Votre invitation sur DORA")
        self.assertIn(
            quote("foo@buzz.com"),
            mail.outbox[0].body,
        )
        self.assertIn(
            f"L’équipe DORA vous a invité(e) à rejoindre la structure { structure.name }",
            mail.outbox[0].body,
        )

    def test_can_invite_multiple_users(self):
        structure = make_structure()
        self.add_row(
            [
                structure.name,
                structure.siret,
                "",
                "foo@buzz.com,bar@buzz.com",
                "",
                "",
                "",
                "",
            ]
        )
        self.call_command()
        self.assertTrue(User.objects.filter(email="foo@buzz.com").exists())
        self.assertTrue(User.objects.filter(email="bar@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 2)

    def test_can_invite_even_if_theres_already_an_admin(self):
        structure = make_structure()
        user = make_user()
        baker.make(StructureMember, user=user, structure=structure, is_admin=True)
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", "", ""]
        )
        out, err = self.call_command()
        self.assertTrue(
            StructurePutativeMember.objects.filter(
                user__email="foo@buzz.com", structure=structure
            ).exists()
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_new_users_are_automatically_accepted(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        self.assertTrue(
            StructurePutativeMember.objects.filter(
                user__email="foo@buzz.com", invited_by_admin=True
            ).exists()
        )

    def test_idempotent(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)
        out, err = self.call_command()
        self.assertIn("foo@buzz.com a déjà été invité·e", out)
        self.assertEqual(Structure.objects.filter(siret=structure.siret).count(), 1)
        self.assertEqual(User.objects.filter(email="foo@buzz.com").count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_invitee_is_admin(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        self.assertTrue(
            StructurePutativeMember.objects.filter(
                user__email="foo@buzz.com",
                structure=structure,
                invited_by_admin=True,
                is_admin=True,
            ).exists()
        )

    def test_email_is_valid(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo.buzz.com", "", "", "", ""]
        )
        out, err = self.call_command()
        self.assertIn("admins", err)
        self.assertIn("Saisissez une adresse e-mail valide.", err)
        self.assertEqual(User.objects.filter(email="foo.buzz.com").count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_structure_name_is_valid(self):
        structure = make_structure()
        self.add_row(["", structure.siret, "", "foo@buzz.com", "", "", "", ""])
        out, err = self.call_command()
        self.assertIn("name", err)
        self.assertIn("Ce champ ne peut être vide.", err)
        self.assertEqual(User.objects.filter(email="foo@buzz.com").count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_invitee_not_a_valid_user_yet(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        user = User.objects.filter(email="foo@buzz.com").first()
        self.assertFalse(user.is_valid)

    def test_invitee_not_a_valid_member_yet(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        members = StructurePutativeMember.objects.filter(
            user__email="foo@buzz.com", structure=structure
        )
        self.assertTrue(members.exists())
        real_members = StructureMember.objects.filter(
            user__email="foo@buzz.com", structure=structure
        )
        self.assertFalse(real_members.exists())

    def test_can_invite_existing_user(self):
        structure = make_structure()
        user = baker.make(
            "users.User", first_name="foo", last_name="bar", is_valid=True
        )
        self.add_row([structure.name, structure.siret, "", user.email, "", "", "", ""])
        self.call_command()
        self.assertEqual(User.objects.filter(email=user.email).count(), 1)
        user.refresh_from_db()
        self.assertEqual(user.get_full_name(), user.get_full_name())
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[DORA] Votre invitation sur DORA")
        self.assertIn(
            quote(user.email),
            mail.outbox[0].body,
        )
        self.assertEqual(
            StructurePutativeMember.objects.filter(
                user=user, structure=structure
            ).count(),
            1,
        )

    def test_existing_user_stay_valid_user(self):
        structure = make_structure()
        user = baker.make(
            "users.User", first_name="foo", last_name="bar", is_valid=True
        )
        self.add_row([structure.name, structure.siret, "", user.email, "", "", "", ""])
        self.call_command()
        user.refresh_from_db()
        self.assertTrue(user.is_valid)

    def test_existing_user_stay_valid_member(self):
        structure = make_structure()
        user = baker.make(
            "users.User", first_name="foo", last_name="bar", is_valid=True
        )
        member = StructureMember.objects.create(
            structure=structure,
            user=user,
        )
        self.add_row([structure.name, structure.siret, "", user.email, "", "", "", ""])
        self.call_command()
        member.refresh_from_db()

    def test_member_can_be_promoted_to_admin(self):
        structure = make_structure()
        user = baker.make(
            "users.User", first_name="foo", last_name="bar", is_valid=True
        )
        member = StructureMember.objects.create(
            structure=structure, user=user, is_admin=False
        )
        self.add_row([structure.name, structure.siret, "", user.email, "", "", "", ""])
        self.call_command()
        member.refresh_from_db()
        self.assertTrue(member.is_admin)

    def test_create_structure_on_the_fly(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
            parent_name="Parent",
        )
        self.add_row(["Foo", "12345678901234", "", "foo@buzz.com", "", "", "", ""])
        self.call_command()
        self.assertTrue(
            Structure.objects.filter(
                siret="12345678901234", name="My Establishment (Parent)"
            ).exists()
        )

    def test_create_parent_structure_on_the_fly(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
            parent_name="Parent",
        )
        self.add_row(["Foo", "", "12345678901234", "foo@buzz.com", "", "", "", ""])
        self.call_command()
        self.assertTrue(
            Structure.objects.filter(
                siret="12345678901234", name="My Establishment (Parent)"
            ).exists()
        )

    def test_create_new_branch(self):
        structure = make_structure(name="My Structure")
        self.add_row(["Foo", "", structure.siret, "foo@buzz.com", "", "", "", ""])
        self.call_command()
        branches = Structure.objects.filter(parent=structure)
        self.assertEqual(branches.count(), 1)
        branch = branches[0]
        self.assertEqual(branch.name, "Foo")
        self.assertEqual(branch.ape, structure.ape)
        self.assertEqual(branch.siret, None)
        self.assertEqual(branch.creator, User.objects.get_dora_bot())
        self.assertEqual(
            branch.source, StructureSource.objects.get(value="invitations-masse")
        )
        self.assertEqual(branch.parent, structure)

    def test_find_existing_branch(self):
        structure = make_structure(name="My Structure", siret="12345678901234")
        branch = baker.make("Structure", name="Foo", siret=None, parent=structure)
        self.assertEqual(structure.branches.count(), 1)
        self.add_row(["Foo", "", structure.siret, "foo@buzz.com", "", "", "", ""])
        self.call_command()
        self.assertEqual(structure.branches.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            StructurePutativeMember.objects.filter(
                structure=branch, user__email="foo@buzz.com"
            ).count(),
            1,
        )
        self.assertIn(
            f"L’équipe DORA vous a invité(e) à rejoindre la structure { branch.name }",
            mail.outbox[0].body,
        )

    def test_create_new_branch_with_siret(self):
        structure = make_structure(name="My Structure")
        baker.make("Establishment", siret="12345678901234", name="My Establishment")
        self.add_row(
            ["Foo", "12345678901234", structure.siret, "foo@buzz.com", "", "", "", ""]
        )
        self.call_command()
        branches = Structure.objects.filter(parent=structure)
        self.assertEqual(branches.count(), 1)
        branch = branches[0]
        self.assertEqual(branch.name, "Foo")
        self.assertEqual(branch.siret, "12345678901234")
        self.assertEqual(branch.creator, User.objects.get_dora_bot())
        self.assertEqual(
            branch.source, StructureSource.objects.get(value="invitations-masse")
        )
        self.assertEqual(branch.parent, structure)

    def test_user_belong_to_branch(self):
        structure = make_structure(name="My Structure")
        self.add_row(["Foo", "", structure.siret, "foo@buzz.com", "", "", "", ""])

        self.call_command()
        branch = Structure.objects.filter(parent=structure).first()
        self.assertEqual(
            StructurePutativeMember.objects.filter(
                structure=branch, user__email="foo@buzz.com"
            ).count(),
            1,
        )
        self.assertIn(
            f"L’équipe DORA vous a invité(e) à rejoindre la structure { branch.name }",
            mail.outbox[0].body,
        )

    def test_user_doesnt_belong_to_parent(self):
        structure = make_structure(name="My Structure")
        self.add_row(["Foo", "", structure.siret, "foo@buzz.com", "", "", "", ""])

        self.call_command()
        self.assertEqual(
            StructureMember.objects.filter(
                structure=structure, user__email="foo@buzz.com"
            ).count(),
            0,
        )

    def test_parent_admin_are_branch_admins(self):
        parent_structure = make_structure()
        parent_admin = make_user(structure=parent_structure, is_admin=True)
        self.add_row(["branch", "", parent_structure.siret, "", "", "", "", ""])
        self.call_command()
        branches = Structure.objects.filter(parent=parent_structure, name="branch")
        self.assertEqual(branches.count(), 1)
        self.assertTrue(
            StructureMember.objects.filter(
                structure=branches[0], user=parent_admin, is_admin=True
            ).exists()
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(mail.outbox[0].subject, "[DORA] Votre antenne a été créée")

    def test_add_labels(self):
        structure = make_structure()
        baker.make("StructureNationalLabel", value="l1")
        baker.make("StructureNationalLabel", value="l2")
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "l1, l2", "", "", ""]
        )
        self.call_command()
        self.assertTrue(structure.national_labels.filter(value="l1").exists())
        self.assertTrue(structure.national_labels.filter(value="l2").exists())

    def test_add_services(self):
        model = make_model()
        structure = make_structure()
        self.add_row([structure.name, structure.siret, "", "", "", model.slug, "", ""])
        self.call_command()
        self.assertTrue(structure.services.filter(model=model).exists())

    def test_labels_must_exist(self):
        structure = make_structure()
        self.add_row(
            [structure.name, structure.siret, "", "foo@buzz.com", "l1, l2", "", "", ""]
        )
        out, err = self.call_command()
        self.assertIn("Label inconnu l1", err)

    def test_models_must_exist(self):
        structure = make_structure()
        self.add_row(
            [
                structure.name,
                structure.siret,
                "",
                "foo@buzz.com",
                "",
                "mod1,mod2",
                "",
                "",
            ]
        )
        out, err = self.call_command()
        self.assertIn("Modèle inconnu mod1", err)

    def test_wont_duplicate_labels(self):
        l1 = baker.make("StructureNationalLabel", value="l1")
        structure = make_structure()
        structure.national_labels.add(l1)
        self.assertEqual(structure.national_labels.filter(value="l1").count(), 1)
        self.add_row([structure.name, structure.siret, "", "", "l1", "", ""])
        self.call_command()
        self.assertEqual(structure.national_labels.filter(value="l1").count(), 1)

    def test_wont_duplicate_services(self):
        model = make_model()
        structure = make_structure()
        make_service(structure=structure, model=model)
        self.assertEqual(structure.services.filter(model=model).count(), 1)
        self.add_row([structure.name, structure.siret, "", "", "", model.slug, ""])
        self.call_command()
        self.assertEqual(structure.services.filter(model=model).count(), 1)

    # champs optionnels :

    def test_add_phone_number(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
        )

        self.add_row(["Test", "12345678901234", "", "", "", "", "0123456789", ""])
        self.call_command()

        structure = Structure.objects.get(siret="12345678901234")

        assert structure.phone == "0123456789"

    def test_add_structure_email(self):
        baker.make(
            "Establishment",
            siret="12345678900000",
            name="My Establishment",
        )

        self.add_row(
            ["Test", "12345678900000", "", "", "", "", "", "email@structure.com"]
        )
        out, err = self.call_command()
        print(out, err)

        structure = Structure.objects.get(siret="12345678900000")

        assert structure.email == "email@structure.com"
