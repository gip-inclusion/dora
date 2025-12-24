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
        call_command("delete_old_closed_orientation_attachments", stdout=StringIO())

    @patch("dora.orientations.models.default_storage.delete")
    @patch("dora.orientations.models.default_storage.exists", return_value=True)
    def test_should_delete_attachments_for_old_closed_orientations(
        self, mock_exists, mock_delete
    ):
        # Tous les statuts qui doivent être traités par la commande
        closed_statuses = [
            OrientationStatus.ACCEPTED,
            OrientationStatus.MODERATION_REJECTED,
            OrientationStatus.REJECTED,
            OrientationStatus.EXPIRED,
        ]

        # Statuts qui ne doivent PAS être traités par la commande
        open_status = [
            OrientationStatus.PENDING,
            OrientationStatus.MODERATION_PENDING,
        ]

        all_statuses = closed_statuses + open_status

        old_orientations = {}
        recent_orientations = {}
        old_attachment_names = {}
        recent_attachment_names = {}

        with freeze_time(self.starting_date):
            old_processing_date = timezone.now() - relativedelta(months=7)
            recent_processing_date = timezone.now() - relativedelta(months=5)

            # Création d'orientations pour tous les statuts (anciennes et récentes)
            for status in all_statuses:
                old_attachment_name = f"attachment_old_{status.value}.txt"
                recent_attachment_name = f"attachment_recent_{status.value}.txt"

                old_orientations[status] = make_orientation(
                    status=status,
                    processing_date=old_processing_date,
                    beneficiary_attachments=[old_attachment_name],
                )
                old_attachment_names[status] = old_attachment_name

                recent_orientations[status] = make_orientation(
                    status=status,
                    processing_date=recent_processing_date,
                    beneficiary_attachments=[recent_attachment_name],
                )
                recent_attachment_names[status] = recent_attachment_name

        # Vérification initiale
        for orientation in old_orientations.values():
            self.assertEqual(len(orientation.beneficiary_attachments), 1)
        for orientation in recent_orientations.values():
            self.assertEqual(len(orientation.beneficiary_attachments), 1)

        with freeze_time(self.starting_date):
            self.call_command()

        # Vérification que les pièces jointes des orientations anciennes fermées ont été supprimées
        for status in closed_statuses:
            old_orientations[status].refresh_from_db()
            self.assertEqual(len(old_orientations[status].beneficiary_attachments), 0)
            mock_delete.assert_any_call(old_attachment_names[status])
        self.assertEqual(mock_delete.call_count, len(closed_statuses))

        # Vérification que les pièces jointes des orientations anciennes ouvertes n'ont PAS été supprimées
        for status in open_status:
            old_orientations[status].refresh_from_db()
            self.assertEqual(len(old_orientations[status].beneficiary_attachments), 1)
            attachment_name = old_attachment_names[status]
            self.assertNotIn(
                attachment_name,
                [call[0][0] for call in mock_delete.call_args_list],
                f"La pièce jointe {attachment_name} ne devrait pas avoir été supprimée",
            )

        # Vérification que les pièces jointes des orientations récentes n'ont PAS été supprimées
        for status in all_statuses:
            recent_orientations[status].refresh_from_db()
            self.assertEqual(
                len(recent_orientations[status].beneficiary_attachments), 1
            )
            attachment_name = recent_attachment_names[status]
            self.assertNotIn(
                attachment_name,
                [call[0][0] for call in mock_delete.call_args_list],
                f"La pièce jointe {attachment_name} ne devrait pas avoir été supprimée",
            )
