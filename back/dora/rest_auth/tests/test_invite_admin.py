from urllib.parse import quote

import pytest
from django.core import mail
from model_bakery import baker

from dora.core.constants import SIREN_FRANCE_TRAVAIL
from dora.core.test_utils import make_structure, make_user
from dora.structures.models import Structure, StructureMember, StructurePutativeMember

TEST_SIRET = "12345678901234"


@pytest.fixture(autouse=True)
def test_establishment():
    baker.make("Establishment", siret=TEST_SIRET)


def test_manager_can_invite(api_client):
    assert not Structure.objects.filter(siret=TEST_SIRET).exists()
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 201
    assert Structure.objects.filter(siret=TEST_SIRET).exists()
    structure = Structure.objects.get(siret=TEST_SIRET)
    member = StructurePutativeMember.objects.get(
        structure__siret=TEST_SIRET, user__email="foo@bar.com"
    )
    assert member.is_admin is True
    assert member.invited_by_admin is True
    assert len(mail.outbox) == 1
    assert "[DORA] Votre invitation sur DORA" in mail.outbox[0].subject
    assert user.get_full_name() in mail.outbox[0].body
    assert "/auth/invitation?" in mail.outbox[0].body
    assert structure.slug in mail.outbox[0].body
    assert quote("foo@bar.com") in mail.outbox[0].body
    assert "foo@bar.com" in mail.outbox[0].to


def test_can_invite_to_existing_structure(api_client):
    make_structure(siret=TEST_SIRET)
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 201
    assert len(mail.outbox) == 1


def test_anonymous_cant_invite(api_client):
    api_client.force_authenticate(user=None)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 401
    assert len(mail.outbox) == 0


def test_normal_user_cant_invite(api_client):
    user = make_user(is_staff=False, is_manager=False)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 403
    assert len(mail.outbox) == 0


def test_admin_cant_invite(api_client):
    structure = make_structure(siret=TEST_SIRET)
    user = make_user(
        structure=structure, is_staff=False, is_manager=False, is_admin=True
    )

    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 403
    assert len(mail.outbox) == 0


def test_superuser_can_invite(api_client):
    user = make_user(is_staff=True)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 201
    assert len(mail.outbox) == 1


def test_siret_is_mandatory(api_client):
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 400
    assert len(mail.outbox) == 0


def test_invitee_email_is_mandatory(api_client):
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET},
    )
    assert response.status_code == 400
    assert len(mail.outbox) == 0


def test_cant_invite_non_pe_agents_to_pe_structure(api_client):
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    siret_pe = SIREN_FRANCE_TRAVAIL + "12345"
    baker.make("Establishment", siret=siret_pe)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": siret_pe, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 403
    assert len(mail.outbox) == 0


def test_can_invite_pe_agents_to_pe_structure_pe_address(api_client):
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    siret_pe = SIREN_FRANCE_TRAVAIL + "12345"
    baker.make("Establishment", siret=siret_pe)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": siret_pe, "invitee_email": "foo@pole-emploi.fr"},
    )
    assert response.status_code == 201
    assert len(mail.outbox) == 1


def test_can_invite_pe_agents_to_pe_structure_ft_address(api_client):
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    siret_pe = SIREN_FRANCE_TRAVAIL + "12345"
    baker.make("Establishment", siret=siret_pe)
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": siret_pe, "invitee_email": "foo@francetravail.fr"},
    )
    assert response.status_code == 201
    assert len(mail.outbox) == 1


def test_cant_invite_other_admins(api_client):
    structure = make_structure(siret=TEST_SIRET)
    make_user(structure=structure, is_staff=False, is_manager=False, is_admin=True)
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": "foo@bar.com"},
    )
    assert response.status_code == 400
    assert "Cette structure a déjà un administrateur" in response.content.decode()
    assert len(mail.outbox) == 0


def test_cant_reinvite_already_existing_admin(api_client):
    structure = make_structure(siret=TEST_SIRET)
    admin = make_user(
        structure=structure, is_staff=False, is_manager=False, is_admin=True
    )
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": admin.email},
    )
    assert response.status_code == 400
    assert "Cette structure a déjà un administrateur" in response.content.decode()
    assert len(mail.outbox) == 0


def test_promote_already_invited_user(api_client):
    existing_user = make_user(is_staff=False, is_manager=False)
    structure = make_structure(siret=TEST_SIRET)
    assert (
        StructurePutativeMember.objects.filter(
            structure=structure, user=existing_user
        ).exists()
        is False
    )
    baker.make(
        "StructurePutativeMember",
        structure=structure,
        user=existing_user,
        invited_by_admin=True,
        is_admin=False,
    )
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": existing_user.email},
    )
    assert response.status_code == 201
    pm = StructurePutativeMember.objects.get(structure=structure, user=existing_user)
    assert pm.is_admin is True
    assert pm.is_admin is True
    assert len(mail.outbox) == 1


def test_promote_already_existing_member(api_client):
    structure = make_structure(siret=TEST_SIRET)
    existing_user = make_user(
        structure=structure, is_staff=False, is_manager=False, is_admin=False
    )
    assert (
        StructureMember.objects.get(structure=structure, user=existing_user).is_admin
        is False
    )
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": existing_user.email},
    )
    assert response.status_code == 201
    assert (
        StructureMember.objects.get(structure=structure, user=existing_user).is_admin
        is True
    )
    assert len(mail.outbox) == 0


def test_accept_and_promote_waiting_member(api_client):
    existing_user = make_user(is_staff=False, is_manager=False)
    structure = make_structure(siret=TEST_SIRET)
    assert (
        StructurePutativeMember.objects.filter(
            structure=structure, user=existing_user
        ).exists()
        is False
    )
    baker.make(
        StructurePutativeMember,
        structure=structure,
        user=existing_user,
        invited_by_admin=False,
    )
    user = make_user(is_staff=False, is_manager=True, departments=[31])
    api_client.force_authenticate(user=user)
    response = api_client.post(
        "/auth/invite-first-admin/",
        {"siret": TEST_SIRET, "invitee_email": existing_user.email},
    )
    assert response.status_code == 201
    pm = StructurePutativeMember.objects.get(structure=structure, user=existing_user)
    assert pm.is_admin is True
    assert pm.invited_by_admin is True
    assert len(mail.outbox) == 1
