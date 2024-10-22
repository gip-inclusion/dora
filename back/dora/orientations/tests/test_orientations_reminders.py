from datetime import timedelta
from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APITestCase

from dora.core.test_utils import make_orientation, make_service, make_structure


class OrientationsNotificationsTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()
        self.service = make_service(structure=self.structure)

    def call_command(self):
        call_command("send_orientations_reminders", stdout=StringIO())

    def test_old_orientations_notified(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            make_orientation()
        self.call_command()
        self.assertGreater(len(mail.outbox), 0)

    def test_old_orientations_structure_notified(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            orientation = make_orientation()
        self.call_command()
        self.assertEqual(mail.outbox[0].to, [orientation.get_contact_email()])
        self.assertEqual(
            mail.outbox[0].subject, "Relance – Demande d’orientation en attente"
        )

    def test_old_orientations_prescriber_notified(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            orientation = make_orientation()
        self.call_command()
        self.assertEqual(mail.outbox[1].to, [orientation.prescriber.email])
        self.assertEqual(
            mail.outbox[1].subject, "Relance envoyée – Demande d’orientation en attente"
        )

    def test_old_orientations_referent_cced(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            orientation = make_orientation()
        self.call_command()
        self.assertEqual(mail.outbox[1].cc, [orientation.referent_email])
        self.assertEqual(
            mail.outbox[1].subject, "Relance envoyée – Demande d’orientation en attente"
        )

    def test_recent_orientations_not_notified(self):
        with freeze_time(timezone.now() - timedelta(days=7)):
            make_orientation()
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)

    def test_old_orientations_notified_at_most_once(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            make_orientation()
        self.call_command()
        self.assertEqual(len(mail.outbox), 2)
        mail.outbox = []
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)

    def test_old_orientations_renotified_after_period(self):
        with freeze_time(timezone.now() - timedelta(days=30)):
            make_orientation()
        with freeze_time(timezone.now() - timedelta(days=19)):
            self.call_command()
            self.assertEqual(len(mail.outbox), 2)
            mail.outbox = []
        with freeze_time(timezone.now() - timedelta(days=15)):
            self.call_command()
            self.assertEqual(len(mail.outbox), 0)
        with freeze_time(timezone.now() - timedelta(days=8)):
            self.call_command()
            self.assertEqual(len(mail.outbox), 2)

    def test_attachments_listed_in_prescriber_message(self):
        with freeze_time(timezone.now() - timedelta(days=11)):
            make_orientation(beneficiary_attachments=["test/hello.pdf"])

        self.call_command()
        self.assertIn("hello.pdf", mail.outbox[1].body)
