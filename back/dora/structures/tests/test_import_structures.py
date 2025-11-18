import csv
import io
from urllib.parse import quote

import pytest
from django.core import mail
from django.core.management import call_command
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import make_model, make_service, make_structure, make_user
from dora.structures.csv_import import ImportStructuresHelper
from dora.structures.models import (
    Structure,
    StructureMember,
    StructurePutativeMember,
    StructureSource,
)
from dora.users.models import User


@pytest.mark.parametrize("wet_run", [True, False])
def test_management_command(caplog, capsys, tmp_path, snapshot, wet_run):
    baker.make(
        "Establishment",
        siret="12345678901234",
        name="My Establishment",
        parent_name="Parent",
    )
    csv_file = tmp_path.joinpath("file_name.csv")
    csv_file.write_text(
        "\n".join(
            [
                "nom,siret,siret_parent,courriels_administrateurs,labels,modeles,telephone,courriel_structure",
                "Foo,12345678901234,,foo@buzz.com,,,,email@structure.com",
            ]
        )
    )

    assert not Structure.objects.filter(siret="12345678901234").exists()
    command_args = [csv_file.as_posix()]
    if wet_run:
        command_args.append("--wet-run")
    call_command("import_structures", *command_args)

    assert Structure.objects.filter(siret="12345678901234").exists() is wet_run
    assert caplog.messages == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")


class StructuresImportTestCase(APITestCase):
    def setUp(self):
        self.import_structures_helper = ImportStructuresHelper()
        self.importing_user = baker.make(
            "users.User", first_name="Test", last_name="User"
        )
        self.csv_headers = "nom,siret,siret_parent,courriels_administrateurs,labels,modeles,telephone,courriel_structure"
        self.source_info = {
            "value": "invitations-masse",
            "label": "Invitations en masse",
        }

    # Validitation du CSV

    def test_unknown_siret_wont_create_anything(self):
        csv_content = (
            f"{self.csv_headers}\nfoo, 12345678901234, '', foo@buzz.com, '', '', '', ''"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(
            "Siret inconnu: https://annuaire-entreprises.data.gouv.fr/etablissement/12345678901234",
            result["errors_map"][2][0],
        )
        self.assertFalse(Structure.objects.filter(siret="12345678901234").exists())
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_siret_wont_create_anything(self):
        csv_content = f"{self.csv_headers}\nfoo,1234,,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )
        self.assertIn(
            "Le numéro SIRET doit être composé de 14 chiffres.",
            result["errors_map"][2][0],
        )
        self.assertFalse(Structure.objects.filter(siret="12345").exists())
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_invalid_parent_siret_error(self):
        csv_content = f"{self.csv_headers}\nfoo,,1234,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "Le numéro SIRET doit être composé de 14 chiffres.",
            result["errors_map"][2][0],
        )
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_unknown_parent_siret_error(self):
        csv_content = f"{self.csv_headers}\nfoo,,12345678901234,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "SIRET parent inconnu",
            result["errors_map"][2][0],
        )
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_missing_siret_error(self):
        csv_content = f"{self.csv_headers}\nfoo,,,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "`siret` ou `parent_siret` sont requis",
            result["errors_map"][2][0],
        )
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_no_recursive_branch(self):
        parent = make_structure()
        make_structure(parent=parent, siret="12345678901234")

        csv_content = f"{self.csv_headers}\nfoo,,12345678901234,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "Le SIRET 12345678901234 est une antenne, il ne peut pas être utilisé comme parent",
            result["errors_map"][2][0],
        )
        self.assertFalse(User.objects.filter(email="foo@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 0)

    def test_check_missing_headers(self):
        csv_content = "invalid,wrong,siret_parent,courriels_administrateurs,labels,modeles,telephone,courriel_structure\n"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "Votre fichier CSV ne contient pas toutes les colonnes requises. Ajoutez les colonnes suivantes :<br/>",
            result["errors_map"][1][0],
        )
        self.assertIn(
            "• nom",
            result["errors_map"][1][0],
        )
        self.assertIn(
            "• siret",
            result["errors_map"][1][0],
        )

    def test_non_unique_source_label_wet_run(self):
        structure = make_structure()

        baker.make("StructureSource", value="test-source", label="Test Source")

        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.assertEqual(Structure.objects.filter(siret=structure.siret).count(), 1)

        source_info = {
            "value": "test-source",
            "label": "New Label",
        }
        result = self.import_structures_helper.import_structures(
            reader,
            self.importing_user,
            source_info,
            wet_run=True,
        )

        self.assertEqual(
            result["errors_map"][1][0],
            'Le fichier nommé "test-source" a déjà un nom de source stocké dans le base de données. Veuillez refaire l\'import avec un nouveau nom de source.',
        )
        self.assertEqual(Structure.objects.filter(siret=structure.siret).count(), 1)
        self.assertEqual(StructureSource.objects.filter(**source_info).count(), 0)

    def test_source_label_not_created_when_errors_wet_run(self):
        csv_content = (
            f"{self.csv_headers}\nTest,12345678900000,,,,,,email1@structure.com"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader,
            self.importing_user,
            {
                "value": "test-source",
                "label": "New Label",
            },
            wet_run=True,
        )

        self.assertEqual(
            len(result["errors_map"].values()),
            1,
        )
        self.assertEqual(StructureSource.objects.filter(value="test-source").count(), 0)

    # Invitations des nouveaux utilisateurs

    def test_can_invite_new_user(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 0)
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
            f"L’équipe DORA vous a invité(e) à rejoindre la structure {structure.name}",
            mail.outbox[0].body,
        )

    def test_can_invite_multiple_users(self):
        structure = make_structure()
        csv_content = f'{self.csv_headers}\n{structure.name},{structure.siret},,"foo@buzz.com,bar@buzz.com",,,,,'
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 0)

        self.assertTrue(User.objects.filter(email="foo@buzz.com").exists())
        self.assertTrue(User.objects.filter(email="bar@buzz.com").exists())
        self.assertEqual(len(mail.outbox), 2)

    def test_can_invite_even_if_theres_already_an_admin(self):
        structure = make_structure()
        user = make_user()
        baker.make(StructureMember, user=user, structure=structure, is_admin=True)
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertTrue(
            StructurePutativeMember.objects.filter(
                user__email="foo@buzz.com", structure=structure, is_admin=True
            ).exists()
        )
        self.assertEqual(len(mail.outbox), 1)

    def test_new_users_are_automatically_accepted(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertTrue(
            StructurePutativeMember.objects.filter(
                user__email="foo@buzz.com", invited_by_admin=True
            ).exists()
        )

    def test_idempotent(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(len(mail.outbox), 1)

        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(Structure.objects.filter(siret=structure.siret).count(), 1)
        self.assertEqual(User.objects.filter(email="foo@buzz.com").count(), 1)
        self.assertEqual(len(mail.outbox), 1)

    def test_invitee_is_admin(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

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
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo.buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn(
            "Saisissez une adresse e-mail valide.", result["errors_map"][2][0]
        )
        self.assertEqual(User.objects.filter(email="foo.buzz.com").count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_structure_name_is_valid(self):
        structure = make_structure()
        csv_content = f"{self.csv_headers}\n,{structure.siret},,foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn('La colonne "nom" est obligatoire', result["errors_map"][2][0])
        self.assertEqual(User.objects.filter(email="foo@buzz.com").count(), 0)
        self.assertEqual(len(mail.outbox), 0)

    def test_invitee_not_a_valid_user_yet(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        user = User.objects.filter(email="foo@buzz.com").first()
        self.assertFalse(user.is_valid)

    def test_invitee_not_a_valid_member_yet(self):
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

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
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,{user.email},,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

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
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,{user.email},,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

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
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,{user.email},,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        member.refresh_from_db()

    def test_member_can_be_promoted_to_admin(self):
        structure = make_structure()
        user = baker.make(
            "users.User", first_name="foo", last_name="bar", is_valid=True
        )
        member = StructureMember.objects.create(
            structure=structure, user=user, is_admin=False
        )
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,{user.email},,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        member.refresh_from_db()
        self.assertTrue(member.is_admin)

    # Création/modification des nouvelles structures/services

    def test_create_structure_on_the_fly(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
            parent_name="Parent",
        )
        csv_content = f"{self.csv_headers}\nFoo,12345678901234,,foo@buzz.com,,,,email@structure.com"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)

        self.assertTrue(
            Structure.objects.filter(
                siret="12345678901234",
                name="My Establishment (Parent)",
                email="email@structure.com",
            ).exists()
        )

    def test_create_parent_structure_on_the_fly(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
            parent_name="Parent",
        )
        csv_content = f"{self.csv_headers}\nFoo,,12345678901234,foo@buzz.com,,,,email@structure.com"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 2)

        parent_structure = Structure.objects.filter(
            siret="12345678901234",
            name="My Establishment (Parent)",
            email="email@structure.com",
        )

        self.assertTrue(parent_structure.exists())

        self.assertTrue(
            Structure.objects.filter(
                name="Foo", parent=parent_structure.first(), email="email@structure.com"
            ).exists()
        )

    def test_create_new_branch(self):
        structure = make_structure(name="My Structure")
        csv_content = f"{self.csv_headers}\nFoo,,{structure.siret},foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)

        branches = Structure.objects.filter(parent=structure)
        self.assertEqual(branches.count(), 1)
        branch = branches[0]
        self.assertEqual(branch.name, "Foo")
        self.assertEqual(branch.ape, structure.ape)
        self.assertEqual(branch.siret, None)
        self.assertEqual(branch.creator, self.importing_user)
        self.assertEqual(
            branch.source, StructureSource.objects.get(value="invitations-masse")
        )
        self.assertEqual(branch.parent, structure)

    def test_find_existing_branch(self):
        structure = make_structure(name="My Structure", siret="12345678901234")
        branch = baker.make("Structure", name="Foo", siret=None, parent=structure)
        self.assertEqual(structure.branches.count(), 1)
        csv_content = f"{self.csv_headers}\nFoo,,{structure.siret},foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(structure.branches.count(), 1)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            StructurePutativeMember.objects.filter(
                structure=branch, user__email="foo@buzz.com"
            ).count(),
            1,
        )
        self.assertIn(
            f"L’équipe DORA vous a invité(e) à rejoindre la structure {branch.name}",
            mail.outbox[0].body,
        )

    def test_create_new_branch_with_siret(self):
        structure = make_structure(name="My Structure")
        baker.make("Establishment", siret="12345678901234", name="My Establishment")
        csv_content = (
            f"{self.csv_headers}\nFoo,12345678901234,{structure.siret},foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)

        branches = Structure.objects.filter(parent=structure)
        self.assertEqual(branches.count(), 1)
        branch = branches[0]
        self.assertEqual(branch.name, "Foo")
        self.assertEqual(branch.siret, "12345678901234")
        self.assertEqual(branch.creator, self.importing_user)
        self.assertEqual(
            branch.source, StructureSource.objects.get(value="invitations-masse")
        )
        self.assertEqual(branch.parent, structure)

    def test_user_belong_to_branch(self):
        structure = make_structure(name="My Structure")
        csv_content = f"{self.csv_headers}\nFoo,,{structure.siret},foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        branch = Structure.objects.filter(parent=structure).first()
        self.assertEqual(
            StructurePutativeMember.objects.filter(
                structure=branch, user__email="foo@buzz.com"
            ).count(),
            1,
        )
        self.assertIn(
            f"L’équipe DORA vous a invité(e) à rejoindre la structure {branch.name}",
            mail.outbox[0].body,
        )

    def test_user_doesnt_belong_to_parent(self):
        structure = make_structure(name="My Structure")
        csv_content = f"{self.csv_headers}\nFoo,,{structure.siret},foo@buzz.com,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(
            StructureMember.objects.filter(
                structure=structure, user__email="foo@buzz.com"
            ).count(),
            0,
        )

    def test_parent_admin_are_branch_admins(self):
        parent_structure = make_structure()
        parent_admin = make_user(structure=parent_structure, is_admin=True)
        csv_content = f"{self.csv_headers}\nbranch,,{parent_structure.siret},,,,,"
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

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
        csv_content = f'{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,"l1, l2",,,'
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertTrue(structure.national_labels.filter(value="l1").exists())
        self.assertTrue(structure.national_labels.filter(value="l2").exists())

    def test_add_services(self):
        model = make_model()
        structure = make_structure()
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,,,{model.slug},,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_services_count"], 1)
        self.assertTrue(structure.services.filter(model=model).exists())

    def test_labels_must_exist(self):
        structure = make_structure()
        csv_content = f'{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,"l1, l2",,,'
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn("Label inconnu l1", result["errors_map"][2][0])

    def test_models_must_exist(self):
        structure = make_structure()
        csv_content = f'{self.csv_headers}\n{structure.name},{structure.siret},,foo@buzz.com,,"mod1,mod2",,'
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertIn("Modèle inconnu mod1", result["errors_map"][2][0])

    def test_wont_duplicate_labels(self):
        l1 = baker.make("StructureNationalLabel", value="l1")
        model = make_model()
        structure = make_structure()
        structure.national_labels.add(l1)
        self.assertEqual(structure.national_labels.filter(value="l1").count(), 1)
        csv_content = (
            f"{self.csv_headers}\n{structure.name},{structure.siret},,,{model.slug},"
        )
        reader = csv.reader(io.StringIO(csv_content))
        self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(structure.national_labels.filter(value="l1").count(), 1)

    def test_wont_duplicate_services(self):
        model = make_model()
        structure = make_structure()
        make_service(structure=structure, model=model)
        self.assertEqual(structure.services.filter(model=model).count(), 1)
        csv_content = f"{self.csv_headers}\n{structure.name}, {structure.siret}, '', '', '', {model.slug}, ''"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 0)

        self.assertEqual(structure.services.filter(model=model).count(), 1)

    def test_add_phone_number_to_new_structure(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
        )
        csv_content = f"{self.csv_headers}\nTest,12345678901234,,,,,0123456789,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)

        structure = Structure.objects.get(siret="12345678901234")

        self.assertEqual(structure.phone, "0123456789")

    def test_add_email_to_new_structure(self):
        baker.make(
            "Establishment",
            siret="12345678900000",
            name="My Establishment",
        )

        csv_content = (
            f"{self.csv_headers}\nTest,12345678900000,,,,,,email@structure.com"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)

        structure = Structure.objects.get(siret="12345678900000")

        self.assertEqual(structure.email, "email@structure.com")

    @freeze_time("2022-01-01")
    def test_modify_phone_of_existing_structure(self):
        structure = make_structure(siret="12345678900000", phone="0123456789")

        csv_content = f"{self.csv_headers}\nTest,12345678900000,,,,,0234567891,"
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["edited_structures_count"], 1)

        structure.refresh_from_db()
        self.assertEqual(structure.phone, "0234567891")
        self.assertEqual(structure.last_editor, self.importing_user)
        self.assertEqual(str(structure.modification_date), "2022-01-01 00:00:00+00:00")

    @freeze_time("2022-01-01")
    def test_modify_email_of_existing_structure(self):
        structure = make_structure(siret="12345678900000", email="old@email.com")

        csv_content = (
            f"{self.csv_headers}\nTest,12345678900000,,,,,,email1@structure.com"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["edited_structures_count"], 1)

        structure.refresh_from_db()
        self.assertEqual(structure.email, "email1@structure.com")
        self.assertEqual(structure.last_editor, self.importing_user)
        self.assertEqual(str(structure.modification_date), "2022-01-01 00:00:00+00:00")

    def test_add_email_to_new_structure_with_parent(self):
        parent = make_structure(siret="21345678900000", email="old@email.com")

        csv_content = (
            f"{self.csv_headers}\nTest,,21345678900000,,,,,email1@structure.com"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_structures_count"], 1)
        self.assertEqual(result["edited_structures_count"], 0)

        new_structure = Structure.objects.get(parent=parent)

        parent.refresh_from_db()
        self.assertEqual(new_structure.email, "email1@structure.com")
        self.assertEqual(parent.email, "old@email.com")

    def test_modify_email_of_existing_structure_with_parent(self):
        parent = make_structure(siret="21345678900000", email="old@email.com")
        branch = make_structure(
            siret="12345678900000", email="other_old@email.com", parent=parent
        )

        csv_content = (
            f"{self.csv_headers}\nTest,12345678900000,,,,,,email1@structure.com"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["edited_structures_count"], 1)

        parent.refresh_from_db()
        branch.refresh_from_db()
        self.assertEqual(branch.email, "email1@structure.com")
        self.assertEqual(parent.email, "old@email.com")

    def test_remove_first_two_lines(self):
        baker.make(
            "Establishment",
            siret="12345678901234",
            name="My Establishment",
            parent_name="Parent",
        )

        csv_content = (
            f"instruction, line, 1\ninstruction, line ,2 \n"
            f"{self.csv_headers}\nFoo,12345678901234,,foo@buzz.com,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))
        result = self.import_structures_helper.import_structures(
            reader,
            self.importing_user,
            self.source_info,
            wet_run=True,
            should_remove_first_two_lines=True,
        )

        self.assertEqual(len(result["errors_map"].keys()), 0)
        self.assertEqual(result["created_structures_count"], 1)
