import csv
import io
from unittest import TestCase

from model_bakery import baker

from dora.service_suggestions.tests import DUMMY_SUGGESTION
from dora.services.management.commands.import_services import import_services
from dora.services.models import Service


class ImportServicesTestCase(TestCase):
    def setUp(self):
        self.importing_user = baker.make("users.User")
        self.csv_headers = "modele_slug,structure_siret,contact_email,label_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement,location_postal_code,diffusion_zone_type"
        self.structure = baker.make("Structure", siret=DUMMY_SUGGESTION["siret"])

        self.service_model = baker.make(
            "Service",
            is_model=True,
            slug="test-service-model",
            name="test-service",
            structure=self.structure,
        )

        self.funding_label = baker.make(
            "FundingLabel", value="test-value", label="test-label"
        )

    def test_import_services_wet_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,Commune"
        )
        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        created_service = Service.objects.get(creator=self.importing_user)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["geo_data_missing_lines"], [])

        self.assertEqual(created_service.structure, self.structure)
        self.assertEqual(created_service.model, self.service_model)
        self.assertEqual(created_service.contact_email, "referent@email.com")

        self.assertEqual(created_service.funding_labels.count(), 1)
        self.assertEqual(
            created_service.funding_labels.first().value, self.funding_label.value
        )

    def test_import_services_dry_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},fake@email.com,{self.funding_label.value},,,,,,,,Commune"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=False)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["error_count"], 0)
        self.assertEqual(result["geo_data_missing_lines"], [])

        self.assertEqual(
            Service.objects.filter(contact_email="fake@email.com").count(), 0
        )
