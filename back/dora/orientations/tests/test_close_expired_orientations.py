from datetime import timedelta
from io import StringIO
from unittest.mock import patch

from django.core import mail
from django.core.management import call_command
from django.test import TransactionTestCase, override_settings
from django.utils import timezone
from freezegun import freeze_time

from dora.core.test_utils import make_orientation
from dora.orientations.models import OrientationStatus


@override_settings(ORIENTATION_EXPIRATION_PERIOD_DAYS=30)
class CloseExpiredOrientationsTestCase(TransactionTestCase):
    def setUp(self):
        self.beneficiary_email = "test@email.com"
        self.starting_date = "2022-01-28"

        with freeze_time(self.starting_date):
            self.orientation_1_start_date = timezone.now() - timedelta(days=31)
            self.expired_orientation_1 = make_orientation(
                creation_date=self.orientation_1_start_date,
                processing_date=None,
                beneficiary_email=self.beneficiary_email,
            )

            self.orientation_2_start_date = timezone.now() - timedelta(days=41)

            self.expired_orientation_2 = make_orientation(
                creation_date=timezone.now() - timedelta(days=51),
                processing_date=self.orientation_2_start_date,
            )

    @staticmethod
    def call_command():
        call_command("close_expired_orientations", stdout=StringIO())

    @patch(
        "dora.orientations.management.commands.close_expired_orientations.send_orientation_expiration_emails"
    )
    @patch("dora.orientations.models.Orientation.delete_attachments")
    def test_should_close_expired_orientations_and_send_emails(
        self, mock_delete_attachments, mock_send_emails
    ):
        with freeze_time("2022-02-01"):
            expected_processing_time = timezone.now()

            with self.assertNumQueries(7):
                self.call_command()

            self.expired_orientation_1.refresh_from_db()
            self.assertEqual(
                self.expired_orientation_1.status, OrientationStatus.EXPIRED
            )
            # This proves the command set processing_date, not that it was already this value
            self.assertEqual(
                self.expired_orientation_1.processing_date, expected_processing_time
            )

            self.expired_orientation_2.refresh_from_db()
            self.assertEqual(
                self.expired_orientation_2.status, OrientationStatus.EXPIRED
            )
            self.assertEqual(
                self.expired_orientation_2.processing_date, expected_processing_time
            )

        self.assertEqual(mock_send_emails.call_count, 2)
        self.assertEqual(
            mock_send_emails.call_args_list[0][0][0], self.expired_orientation_1
        )
        self.assertEqual(
            mock_send_emails.call_args_list[0][0][1],
            self.orientation_1_start_date,
        )
        self.assertEqual(
            mock_send_emails.call_args_list[1][0][0], self.expired_orientation_2
        )
        self.assertEqual(
            mock_send_emails.call_args_list[1][0][1],
            self.orientation_2_start_date,
        )

        self.assertEqual(mock_delete_attachments.call_count, 2)

    def test_should_not_close_unexpired_orientations(self):
        with freeze_time(self.starting_date):
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
                self.orientation_in_moderation.status,
                OrientationStatus.MODERATION_PENDING,
            )

    @patch(
        "dora.orientations.management.commands.close_expired_orientations.send_orientation_expiration_emails"
    )
    def test_should_not_send_email_if_orientation_is_too_old(self, mock_send_emails):
        with freeze_time(self.starting_date):
            self.expired_orientation_1.creation_date = timezone.now() - timedelta(
                days=61
            )
            self.expired_orientation_1.save()

            self.expired_orientation_2.creation_date = timezone.now() - timedelta(
                days=61
            )
            self.expired_orientation_2.save()

            self.call_command()
            self.assertEqual(mock_send_emails.call_count, 0)

    def test_should_send_three_emails_when_prescriber_and_referent_are_the_same(
        self,
    ):
        self.expired_orientation_1.referent_email = (
            self.expired_orientation_1.prescriber.email
        )
        self.expired_orientation_1.save()

        # on ne teste qu'une orientation pour simplifier les assertions
        self.expired_orientation_2.status = OrientationStatus.ACCEPTED
        self.expired_orientation_2.save()

        with freeze_time(self.starting_date):
            self.call_command()

        self.assertEqual(len(mail.outbox), 3)

        self.assertEqual(
            mail.outbox[0].to, [self.expired_orientation_1.get_contact_email()]
        )
        self.assertEqual(
            mail.outbox[0].subject, "Cette demande d’orientation a expiré."
        )

        self.assertEqual(mail.outbox[1].to, [self.beneficiary_email])
        self.assertEqual(
            mail.outbox[1].subject, "Cette demande d’orientation a été annulée."
        )

        self.assertEqual(
            mail.outbox[2].to, [self.expired_orientation_1.prescriber.email]
        )
        self.assertEqual(mail.outbox[2].subject, "Votre demande d’orientation a expiré")

    def test_should_send_four_emails_when_prescriber_and_referent_are_different(self):
        self.expired_orientation_1.referent_email = "different-person@email.com"
        self.expired_orientation_1.save()

        # on ne teste qu'une orientation pour simplifier les assertions
        self.expired_orientation_2.status = OrientationStatus.ACCEPTED
        self.expired_orientation_2.save()

        with freeze_time(self.starting_date):
            self.call_command()

        self.assertEqual(len(mail.outbox), 4)

        self.assertEqual(
            mail.outbox[0].to, [self.expired_orientation_1.get_contact_email()]
        )
        self.assertEqual(
            mail.outbox[0].subject, "Cette demande d’orientation a expiré."
        )

        self.assertEqual(mail.outbox[1].to, [self.beneficiary_email])
        self.assertEqual(
            mail.outbox[1].subject, "Cette demande d’orientation a été annulée."
        )

        prescriber_and_referent_emails = mail.outbox[2:4]
        recipients = [email.to[0] for email in prescriber_and_referent_emails]

        self.assertIn(self.expired_orientation_1.prescriber.email, recipients)
        self.assertIn(self.expired_orientation_1.referent_email, recipients)

        for email in prescriber_and_referent_emails:
            self.assertEqual(email.subject, "Votre demande d’orientation a expiré")
