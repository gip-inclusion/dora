from io import StringIO

import pytest
from django.core.management import call_command

from dora.core.test_utils import make_structure, make_user
from dora.users.models import User


@pytest.fixture
def src_user():
    return make_user(email="source@example.com")


@pytest.fixture
def dest_user():
    return make_user(email="dest@example.com")


def test_identical_users():
    # impossible de fusionner deux utilisateurs identiques
    out = StringIO()
    email = "same@example.com"

    call_command("merge_users", email, email, stdout=out)

    assert "Les deux utilisateurs sont identiques" in out.getvalue()


def test_nonexistent_source_user(src_user, dest_user):
    out = StringIO()

    call_command(
        "merge_users", "nonexistent@example.com", "dest@example.com", stdout=out
    )

    assert "Utilisateur 'nonexistent@example.com' introuvable" in out.getvalue()


def test_nonexistent_dest_user(src_user, dest_user):
    out = StringIO()

    call_command(
        "merge_users", "source@example.com", "nonexistent@example.com", stdout=out
    )

    assert "Utilisateur 'nonexistent@example.com' introuvable" in out.getvalue()


def test_merge_memberships(src_user, dest_user):
    # Créer une appartenance pour l'utilisateur source
    structure = make_structure(user=src_user)
    out = StringIO()

    call_command(
        "merge_users", src_user.email, dest_user.email, "--wet-run", stdout=out
    )

    # Vérifier que l'appartenance à la structure a été transférée
    assert (
        dest_user in structure.members.all()
    ), "L'utilisateur doit être membre de la structure"
    assert "Fusion effectuée" in out.getvalue()


def test_merge_invitations(src_user, dest_user):
    # Créer une invitation pour l'utilisateur source
    structure = make_structure(putative_member=src_user)
    out = StringIO()

    call_command(
        "merge_users", src_user.email, dest_user.email, "--wet-run", stdout=out
    )

    # Vérifier que l'invitation a été transférée
    assert (
        dest_user in structure.putative_members.all()
    ), "L'utilisateur doit être invité de la structure"
    assert "Fusion effectuée" in out.getvalue()


def test_delete_source_user(src_user, dest_user):
    out = StringIO()

    call_command(
        "merge_users",
        src_user.email,
        dest_user.email,
        "--wet-run",
        "--delete",
        stdout=out,
    )

    # Vérifier que l'utilisateur source a été supprimé en fin de traitement
    with pytest.raises(User.DoesNotExist):
        User.objects.get(id=src_user.id)


def test_dry_run_mode(src_user, dest_user):
    # verification du dry-run : pas de données enregistrées
    structure = make_structure(user=src_user)
    out = StringIO()

    call_command("merge_users", src_user.email, dest_user.email, stdout=out)

    assert (
        dest_user not in structure.members.all()
    ), "L'utilisateur ne doit pas être membre de la structure"
    assert src_user.is_active, "L'utilisateur doit encore être actif"
    assert "Mode 'dry-run'" in out.getvalue()

    structure = make_structure(putative_member=src_user)
    out = StringIO()

    call_command("merge_users", src_user.email, dest_user.email, stdout=out)

    assert (
        dest_user not in structure.putative_members.all()
    ), "L'utilisateur ne doit pas être invité de la structure"
    assert src_user.is_active, "L'utilisateur doit encore être actif"
    assert "Mode 'dry-run'" in out.getvalue()
