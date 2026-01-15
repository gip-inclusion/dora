import csv
import io
from unittest import TestCase

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
        self.label = baker.make("FundingLabel", value="test-value", label="test-label")
        self.label_services_helper = LabelServicesHelper()

    def test_label_services_wet_run(self):
        csv_content = f"{self.csv_headers}\n{self.service_url},{self.label.label}"
        reader = csv.reader(io.StringIO(csv_content))

        result = self.label_services_helper.label_services(
            reader, self.labeler, source_info=None, wet_run=True
        )

        self.assertEqual(result["labeled_count"], 1)
        self.assertEqual(result["errors"], [])

        self.service.refresh_from_db()
        self.assertEqual(self.service.funding_labels.count(), 1)
        self.assertEqual(self.service.funding_labels.first().value, self.label.value)
        self.assertEqual(self.service.last_editor, self.labeler)
