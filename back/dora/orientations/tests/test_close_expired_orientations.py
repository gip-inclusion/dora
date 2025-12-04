from datetime import timedelta
from io import StringIO
from unittest.mock import patch

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from dora.core.test_utils import make_orientation
from dora.orientations.models import OrientationStatus


@freeze_time("2022-01-01")
@patch(
    "dora.orientations.management.commands.close_expired_orientations.send_orientation_expiration_emails"
)
class CloseExpiredOrientationsTestCase(TestCase):
    def setUp(self):
        self.expired_orientation_1 = make_orientation(
            creation_date=timezone.now() - timedelta(days=31), processing_date=None
        )
        self.expired_orientation_2 = make_orientation(
            creation_date=timezone.now() - timedelta(days=51),
            processing_date=timezone.now() - timedelta(days=41),
        )

    @staticmethod
    def call_command():
        call_command("close_expired_orientations", stdout=StringIO())

    @patch("dora.orientations.models.Orientation.delete_attachments")
    def test_should_close_expired_orientations_and_send_emails(
        self, mock_delete_attachments, mock_send_emails
    ):
        with self.assertNumQueries(2):
            self.call_command()

        self.expired_orientation_1.refresh_from_db()
        self.assertEqual(self.expired_orientation_1.status, OrientationStatus.EXPIRED)
        self.assertEqual(self.expired_orientation_1.processing_date, timezone.now())
        self.assertEqual(
            self.expired_orientation_1.last_reminder_email_sent, timezone.now()
        )

        self.expired_orientation_2.refresh_from_db()
        self.assertEqual(self.expired_orientation_2.status, OrientationStatus.EXPIRED)
        self.assertEqual(self.expired_orientation_2.processing_date, timezone.now())
        self.assertEqual(
            self.expired_orientation_2.last_reminder_email_sent, timezone.now()
        )

        self.assertEqual(mock_send_emails.call_count, 2)
        self.assertEqual(
            mock_send_emails.call_args_list[0][0][0], self.expired_orientation_1
        )
        self.assertEqual(
            mock_send_emails.call_args_list[1][0][0], self.expired_orientation_2
        )

        self.assertEqual(mock_delete_attachments.call_count, 2)

    def test_should_not_close_unexpired_orientations(self, mock_send_emails):
        self.valid_orientation = make_orientation(
            creation_date=timezone.now() - timedelta(days=1),
        )
        self.orientation_in_moderation = make_orientation(
            status=OrientationStatus.MODERATION_PENDING,
            creation_date=timezone.now() - timedelta(days=31),
            processing_date=None,
        )

        self.call_command()

        self.valid_orientation.refresh_from_db()
        self.assertEqual(self.valid_orientation.status, OrientationStatus.PENDING)

        self.orientation_in_moderation.refresh_from_db()
        self.assertEqual(
            self.orientation_in_moderation.status, OrientationStatus.MODERATION_PENDING
        )

    def test_should_not_send_email_if_orientation_is_too_old(self, mock_send_emails):
        self.expired_orientation_1.creation_date = timezone.now() - timedelta(days=61)
        self.expired_orientation_1.save()

        self.expired_orientation_2.processing_date = timezone.now() - timedelta(days=61)
        self.expired_orientation_2.save()

        self.call_command()
        self.assertEqual(mock_send_emails.call_count, 0)
