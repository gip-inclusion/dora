from io import StringIO
from unittest.mock import patch

from dateutil.relativedelta import relativedelta
from django.core.management import call_command
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from freezegun import freeze_time

from dora.core.test_utils import make_orientation
from dora.orientations.models import OrientationStatus


@override_settings(ORIENTATION_ATTACHMENTS_EXPIRATION_PERIOD_MONTHS=6)
class DeleteOldAcceptedOrientationAttachmentsTestCase(TransactionTestCase):
    def setUp(self):
        self.starting_date = "2024-01-15"

    @staticmethod
    def call_command():
        call_command("delete_old_accepted_orientation_attachments", stdout=StringIO())

    @patch("dora.orientations.models.default_storage.delete")
    @patch("dora.orientations.models.default_storage.exists")
    def test_should_delete_attachments_for_old_accepted_orientations(
        self, mock_exists, mock_delete
    ):
        mock_exists.return_value = True

        with freeze_time(self.starting_date):
            # Orientation acceptée il y a plus de 6 mois (7 mois)
            old_processing_date = timezone.now() - relativedelta(months=7)
            old_accepted_orientation = make_orientation(
                status=OrientationStatus.ACCEPTED,
                processing_date=old_processing_date,
            )
            old_accepted_orientation.beneficiary_attachments = [
                "old_attachment_1.txt",
                "old_attachment_2.txt",
            ]
            old_accepted_orientation.save()

            # Orientation acceptée il y a moins de 6 mois (5 mois)
            recent_processing_date = timezone.now() - relativedelta(months=5)
            recent_accepted_orientation = make_orientation(
                status=OrientationStatus.ACCEPTED,
                processing_date=recent_processing_date,
            )
            recent_accepted_orientation.beneficiary_attachments = [
                "recent_attachment_1.txt",
                "recent_attachment_2.txt",
            ]
            recent_accepted_orientation.save()

        self.assertEqual(len(old_accepted_orientation.beneficiary_attachments), 2)
        self.assertEqual(len(recent_accepted_orientation.beneficiary_attachments), 2)

        with freeze_time(self.starting_date):
            self.call_command()

        # Vérification que les pièces-jointes de l'orientation ancienne ont été supprimées
        old_accepted_orientation.refresh_from_db()
        self.assertEqual(len(old_accepted_orientation.beneficiary_attachments), 0)
        self.assertEqual(mock_delete.call_count, 2)
        mock_delete.assert_any_call("old_attachment_1.txt")
        mock_delete.assert_any_call("old_attachment_2.txt")

        # Vérification que les pièces-jointes de l'orientation récente n'ont pas été supprimées
        recent_accepted_orientation.refresh_from_db()
        self.assertEqual(len(recent_accepted_orientation.beneficiary_attachments), 2)
