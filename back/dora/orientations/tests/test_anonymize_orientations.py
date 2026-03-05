from datetime import timedelta
from io import StringIO

from django.core.management import call_command
from django.test import TestCase
from django.utils import timezone
from freezegun import freeze_time

from dora.core.test_utils import make_orientation


class AnonymizeOrientationsTestCase(TestCase):
    def setUp(self):
        self.starting_date = "2026-01-01"

        with freeze_time(self.starting_date):
            self.orientation_creation_date = timezone.now() - timedelta(days=731)
            self.orientation = make_orientation(
                creation_date=self.orientation_creation_date,
                beneficiary_first_name="Test",
                beneficiary_last_name="Test",
                beneficiary_phone="Test",
                beneficiary_email="Test",
                beneficiary_france_travail_number="Test",
                referent_first_name="Test",
                referent_last_name="Test",
                referent_phone="Test",
                referent_email="Test",
                di_contact_name="Test",
                di_contact_email="Test",
            )

    @staticmethod
    def call_command():
        call_command("anonymize_orientations", stdout=StringIO())

    def test_should_anonymize_orientations(self):
        with freeze_time(self.starting_date):
            self.call_command()

            self.orientation.refresh_from_db()

            self.assertEqual(self.orientation.beneficiary_first_name, "")
            self.assertEqual(self.orientation.beneficiary_last_name, "")
            self.assertEqual(self.orientation.beneficiary_phone, "")
            self.assertEqual(self.orientation.beneficiary_email, "")
            self.assertEqual(self.orientation.beneficiary_france_travail_number, "")
            self.assertEqual(self.orientation.referent_first_name, "")
            self.assertEqual(self.orientation.referent_last_name, "")
            self.assertEqual(self.orientation.referent_phone, "")
            self.assertEqual(self.orientation.referent_email, "")
            self.assertEqual(self.orientation.di_contact_name, "")
            self.assertEqual(self.orientation.di_contact_email, "")

            self.assertTrue(self.orientation.is_anonymized)

    def test_should_not_anonymize_orientations_newer_than_theperiod(self):
        self.orientation.creation_date = timezone.now()

        self.assertEqual(self.orientation.beneficiary_first_name, "Test")
        self.assertEqual(self.orientation.beneficiary_last_name, "Test")
        self.assertEqual(self.orientation.beneficiary_phone, "Test")
        self.assertEqual(self.orientation.beneficiary_email, "Test")
        self.assertEqual(self.orientation.beneficiary_france_travail_number, "Test")
        self.assertEqual(self.orientation.referent_first_name, "Test")
        self.assertEqual(self.orientation.referent_last_name, "Test")
        self.assertEqual(self.orientation.referent_phone, "Test")
        self.assertEqual(self.orientation.referent_email, "Test")
        self.assertEqual(self.orientation.di_contact_name, "Test")
        self.assertEqual(self.orientation.di_contact_email, "Test")

        self.assertFalse(self.orientation.is_anonymized)
        self.assertIsNone(self.orientation.processing_date, timezone.now())
