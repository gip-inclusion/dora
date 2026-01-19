import csv
import io
from unittest import TestCase

from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker

from dora.core.test_utils import make_service, make_user
from dora.services.label_services import LabelServicesHelper


class LabelServicesTestCase(TestCase):
    def setUp(self):
        self.labeler = make_user()
        self.csv_headers = "service_url,label"
        self.service = make_service()
        self.service_url = (
            f"https://dora.inclusion.gouv.fr/services/{self.service.slug}"
        )
        self.funding_label = baker.make(
            "FundingLabel", value="test-value", label="test-label"
        )
        self.label_services_helper = LabelServicesHelper()

    def test_label_services_wet_run(self):
        csv_content = (
            f"{self.csv_headers}\n{self.service_url},{self.funding_label.label}"
        )
        reader = csv.reader(io.StringIO(csv_content))

        with freeze_time("2026-01-01"):
            result = self.label_services_helper.label_services(
                reader, self.labeler, source_info=None, wet_run=True
            )
            expected_modification_date = timezone.now()

        self.assertEqual(result["labeled_count"], 1)
        self.assertEqual(result["errors"], [])

        self.service.refresh_from_db()
        self.assertEqual(self.service.funding_labels.count(), 1)
        self.assertEqual(
            self.service.funding_labels.first().value, self.funding_label.value
        )
        self.assertEqual(self.service.last_editor, self.labeler)
        self.assertEqual(self.service.modification_date, expected_modification_date)

    def test_label_services_dry_run(self):
        csv_content = (
            f"{self.csv_headers}\n{self.service_url},{self.funding_label.label}"
        )
        reader = csv.reader(io.StringIO(csv_content))

        result = self.label_services_helper.label_services(
            reader, self.labeler, source_info=None, wet_run=False
        )

        self.assertEqual(result["labeled_count"], 1)
        self.assertEqual(result["errors"], [])

        self.service.refresh_from_db()
        self.assertEqual(self.service.funding_labels.count(), 0)

    def test_funding_label_does_not_exist(self):
        csv_content = f"{self.csv_headers}\n{self.service_url},invalid-label\n{self.service_url},{self.funding_label.label}"
        reader = csv.reader(io.StringIO(csv_content))

        result = self.label_services_helper.label_services(
            reader, self.labeler, source_info=None, wet_run=True
        )

        self.assertEqual(result["labeled_count"], 0)
        self.assertEqual(
            result["errors"],
            ["[2] Le label de financement 'invalid-label' n'existe pas."],
        )

        self.service.refresh_from_db()
        self.assertEqual(self.service.funding_labels.count(), 0)

    def test_service_does_not_exist(self):
        csv_content = f"{self.csv_headers}\n{self.service_url},{self.funding_label.label}\ninvalid-service,{self.funding_label.label}\n"
        reader = csv.reader(io.StringIO(csv_content))

        result = self.label_services_helper.label_services(
            reader, self.labeler, source_info=None, wet_run=True
        )

        self.assertEqual(result["labeled_count"], 0)
        self.assertEqual(
            result["errors"],
            ["[3] Le service avec le slug 'invalid-service' n'existe pas."],
        )

        self.service.refresh_from_db()
        self.assertEqual(self.service.funding_labels.count(), 0)

    def test_handles_both_errors_on_same_line(self):
        csv_content = f"{self.csv_headers}\ninvalid-service,invalid-label"
        reader = csv.reader(io.StringIO(csv_content))

        result = self.label_services_helper.label_services(
            reader, self.labeler, source_info=None, wet_run=True
        )

        self.assertEqual(result["labeled_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "[2] Le service avec le slug 'invalid-service' n'existe pas.",
        )

        self.assertEqual(
            result["errors"][1],
            "[2] Le label de financement 'invalid-label' n'existe pas.",
        )
