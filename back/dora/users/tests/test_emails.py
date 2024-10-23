import pytest
from dateutil.relativedelta import relativedelta
from django.core import mail
from django.templatetags.l10n import localize
from django.utils import timezone

from dora.core.test_utils import make_structure, make_user
from dora.users.emails import (
    send_account_deletion_notification,
    send_invitation_reminder,
    send_user_without_structure_notification,
)


@pytest.mark.parametrize("with_notification", (True, False))
def test_send_invitation_reminder(with_notification):
    user = make_user()
    structure = make_structure(putative_member=user)

    send_invitation_reminder(user, structure, notification=with_notification)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user.email]
    assert (
        mail.outbox[0].subject
        == f"Rappel : Acceptez l'invitation à rejoindre {structure.name} sur DORA"
    )
    assert structure.name in mail.outbox[0].body
    assert "/auth/invitation" in mail.outbox[0].body

    if with_notification:
        assert "MailsTransactionnels" in mail.outbox[0].body
        assert "InvitationaConfirmer" in mail.outbox[0].body
    else:
        assert "MailsTransactionnels" not in mail.outbox[0].body
        assert "InvitationaConfirmer" not in mail.outbox[0].body


def test_send_account_deletion_notification():
    user = make_user(email="buzz@lightyear.com")

    send_account_deletion_notification(user)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user.email]
    assert mail.outbox[0].subject == "DORA - Suppression prochaine de votre compte"
    assert (
        localize(timezone.localdate() + relativedelta(days=30)) in mail.outbox[0].body
    )
    assert "/auth/connexion" in mail.outbox[0].body
    assert "MailsTransactionnels" in mail.outbox[0].body
    assert "RelanceInactif" in mail.outbox[0].body


@pytest.mark.parametrize(
    "deletion,subject",
    (
        (False, "Rappel : Identifiez votre structure sur DORA"),
        (True, "Dernier rappel avant suppression"),
    ),
)
def test_send_user_without_structure_notification(deletion, subject):
    user = make_user()

    send_user_without_structure_notification(user, deletion=deletion)

    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [user.email]
    assert mail.outbox[0].subject == subject
    assert user.last_name in mail.outbox[0].body
    assert "MailsTransactionnels" in mail.outbox[0].body
    assert "InscritSansStructure" in mail.outbox[0].body
    assert "Nous avons accès à vos données à caractère personnel" in mail.outbox[0].body
