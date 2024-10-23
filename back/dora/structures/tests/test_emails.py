from dateutil.relativedelta import relativedelta
from django.core import mail
from django.utils import timezone
from django.utils.http import urlencode
from freezegun import freeze_time

from dora.core.test_utils import make_structure, make_user

from ..emails import (
    send_admin_invited_users_20_notification,
    send_admin_invited_users_90_notification,
    send_admin_self_invited_users_notification,
    send_orphan_structure_notification,
    send_structure_activation_notification,
)


def test_send_orphan_structure_notification():
    structure = make_structure(email="woody@pixar.com")

    send_orphan_structure_notification(structure)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [structure.email]
    assert (
        mail.outbox[0].subject
        == f"Votre structure n’a pas encore de membre actif sur DORA ({structure.name})"
    )
    assert structure.name in mail.outbox[0].body
    assert f"/auth/invitation?structure={structure.slug}" in mail.outbox[0].body
    assert "mtm_campaign=MailsTransactionnels" in mail.outbox[0].body
    assert "mtm_kwd=InvitationStructuresOrphelines" in mail.outbox[0].body
    assert "aide.dora.inclusion.beta.gouv.fr" in mail.outbox[0].body
    assert "app.livestorm.co/dora-1/presentation-dora" in mail.outbox[0].body


def test_send_first_admin_notification_for_pending_invitation():
    putative_member = make_user()
    structure = make_structure(putative_member=putative_member)
    admin_users = [
        make_user(structure=structure, is_admin=True),
        make_user(structure=structure, is_admin=True),
    ]

    send_admin_invited_users_20_notification(structure, putative_member)

    assert len(mail.outbox) == len(admin_users)

    for idx, admin_user in enumerate(admin_users):
        assert mail.outbox[idx].to == [admin_user.email]
        assert mail.outbox[idx].subject == "Invitation non acceptée : Action requise"
        assert structure.name in mail.outbox[idx].body
        assert putative_member.email in mail.outbox[idx].body
        assert "aide.dora.inclusion.beta.gouv.fr" in mail.outbox[idx].body
        assert (
            "gerer-le-compte-de-ses-collaborateurs-en-tant-quadministrateur-xkonvm"
            in mail.outbox[idx].body
        )


def test_send_second_admin_notification_for_pending_invitation():
    putative_member = make_user()
    structure = make_structure(putative_member=putative_member)
    admin_users = [
        make_user(structure=structure, is_admin=True),
        make_user(structure=structure, is_admin=True),
    ]

    send_admin_invited_users_90_notification(structure, putative_member)

    assert len(mail.outbox) == len(admin_users)

    for idx, admin_user in enumerate(admin_users):
        assert mail.outbox[idx].to == [admin_user.email]
        assert (
            mail.outbox[idx].subject
            == "Action requise : une de vos invitations sera bientôt désactivée"
        )
        assert structure.name in mail.outbox[idx].body
        assert putative_member.email in mail.outbox[idx].body


def test_send_admin_self_invited_users_notification():
    putative_member = make_user()
    structure = make_structure(putative_member=putative_member)
    admins_users = [
        make_user(structure=structure, is_admin=True),
        make_user(structure=structure, is_admin=True),
    ]

    send_admin_self_invited_users_notification(structure, putative_member)

    assert len(mail.outbox) == 2

    for idx, admin_user in enumerate(admins_users):
        assert mail.outbox[idx].to == [admin_user.email]
        assert mail.outbox[idx].subject == "Rappel : Demande de rattachement en attente"
        assert structure.name in mail.outbox[idx].body
        assert putative_member.email in mail.outbox[idx].body
        assert putative_member.first_name in mail.outbox[idx].body
        assert putative_member.last_name in mail.outbox[idx].body
        assert "/auth/connexion" in mail.outbox[idx].body
        assert (
            urlencode({"next": f"/structures/{structure.slug}/collaborateurs"})
            in mail.outbox[idx].body
        )
        assert "aide.dora.inclusion.beta.gouv.fr" in mail.outbox[idx].body
        assert (
            "gerer-le-compte-de-ses-collaborateurs-en-tant-quadministrateur-xkonvm"
            in mail.outbox[idx].body
        )


def test_send_structure_activation_notification_to_old_admins():
    structure = make_structure()

    # les admins concernés par la notification doivent être inscrits depuis plus d'un mois
    with freeze_time(time_to_freeze=timezone.now() - relativedelta(months=2)):
        admin_users = [
            make_user(structure=structure, is_admin=True),
            make_user(structure=structure, is_admin=True),
        ]

    send_structure_activation_notification(structure)

    assert len(mail.outbox) == len(admin_users)

    for idx, admin_user in enumerate(admin_users):
        assert mail.outbox[idx].to == [admin_user.email]
        assert (
            mail.outbox[idx].subject
            == f"Votre structure n’a pas encore publié de service sur DORA ({structure.name})"
        )
        assert structure.name in mail.outbox[idx].body
        assert (
            urlencode({"next": f"/structures/{structure.slug}/services"})
            in mail.outbox[idx].body
        )
        assert "mtm_campaign=MailsTransactionnels" in mail.outbox[idx].body
        assert "mtm_kwd=RelanceActivationService" in mail.outbox[idx].body
        assert "aide.dora.inclusion.beta.gouv.fr" in mail.outbox[idx].body
        assert "app.livestorm.co/dora-1/presentation-dora" in mail.outbox[idx].body


def test_send_structure_activation_notification_to_other_members():
    structure = make_structure()
    make_user(structure, is_admin=True)

    send_structure_activation_notification(structure)

    # les nouveaux admins et utilisateurs ne sont pas concernés par la notification
    assert not len(mail.outbox)

    make_user(structure)
    send_structure_activation_notification(structure)

    assert not len(mail.outbox)
