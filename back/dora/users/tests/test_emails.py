from unittest import TestCase
from unittest.mock import patch

import pytest
from dateutil.relativedelta import relativedelta
from django.core import mail
from django.templatetags.l10n import localize
from django.utils import timezone

from dora.core.models import ModerationStatus
from dora.core.test_utils import make_structure, make_user
from dora.users.emails import (
    send_account_deletion_notification,
    send_invitation_reminder,
    send_user_without_structure_notification,
    send_weekly_email_to_department_managers,
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


@patch("dora.users.emails.send_mail")
class SendWeeklyDepartmentManagerEmail(TestCase):
    def setUp(self):
        self.department = "42"
        self.manager = make_user(is_manager=True, departments=[self.department])

    def test_send_email_with_structures_awaiting_moderation(self, mock_send_email):
        structure_awaiting_moderation = make_structure(
            department=self.department,
            moderation_status=ModerationStatus.NEED_NEW_MODERATION,
            user=make_user(),
        )

        send_weekly_email_to_department_managers(self.manager)

        mock_send_email.assert_called_once()
        self.assertEqual(
            mock_send_email.call_args[0][0],
            "DORA - Vous avez des structures à modérer cette semaine",
        )
        self.assertEqual(mock_send_email.call_args[0][1], self.manager.email)
        self.assertIn(
            f"<p>À valider :</p><ul><li>{structure_awaiting_moderation.name}</li></ul>",
            mock_send_email.call_args[0][2],
        )
        self.assertIn("1 structure(s) en attente", mock_send_email.call_args[0][2])

    def test_send_email_with_orphaned_structures(self, mock_send_email):
        orphaned_structure = make_structure(
            department=self.department,
            user=None,
            putative_member=None,
            moderation_status=ModerationStatus.VALIDATED,
        )

        send_weekly_email_to_department_managers(self.manager)

        mock_send_email.assert_called_once()
        self.assertEqual(
            mock_send_email.call_args[0][0],
            "DORA - Vous avez des structures à modérer cette semaine",
        )
        self.assertEqual(mock_send_email.call_args[0][1], self.manager.email)
        self.assertIn(
            f"<p>Sans utilisateur :</p><ul><li>{orphaned_structure.name}</li></ul>",
            mock_send_email.call_args[0][2],
        )
        self.assertIn("1 structure(s) en attente", mock_send_email.call_args[0][2])

    def test_do_not_send_email_with_no_structures(self, mock_send_email):
        make_structure(
            department=self.department,
            moderation_status=ModerationStatus.VALIDATED,
            user=make_user(),
        )

        send_weekly_email_to_department_managers(self.manager)

        mock_send_email.assert_not_called()

    def test_structures_listed_in_alphabetical_order_and_in_correct_categories(
        self, mock_send_email
    ):
        make_structure(
            department=self.department,
            user=None,
            putative_member=None,
            moderation_status=ModerationStatus.NEED_NEW_MODERATION,
            name="Alpha",
        )

        make_structure(
            department=self.department,
            user=None,
            putative_member=None,
            moderation_status=ModerationStatus.NEED_INITIAL_MODERATION,
            name="Zeta",
        )

        send_weekly_email_to_department_managers(self.manager)

        mock_send_email.assert_called_once()
        self.assertEqual(
            mock_send_email.call_args[0][0],
            "DORA - Vous avez des structures à modérer cette semaine",
        )
        self.assertEqual(mock_send_email.call_args[0][1], self.manager.email)
        self.assertIn(
            "<p>À valider :</p><ul><li>Alpha</li><li>Zeta</li>"
            "</ul><p>Sans utilisateur :</p>"
            "<ul><li>Alpha</li><li>Zeta</li></ul></p>",
            mock_send_email.call_args[0][2],
        )
        self.assertIn("4 structure(s) en attente", mock_send_email.call_args[0][2])
