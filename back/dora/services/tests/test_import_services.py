import csv
import io
from unittest import TestCase
from unittest.mock import patch

from django.contrib.gis.geos import Point
from model_bakery import baker

from dora.core.utils import GeoData
from dora.service_suggestions.tests import DUMMY_SUGGESTION
from dora.services.enums import ServiceStatus
from dora.services.management.commands.import_services import import_services
from dora.services.models import Service, ServiceSource


class ImportServicesTestCase(TestCase):
    def setUp(self):
        self.importing_user = baker.make("users.User")
        self.csv_headers = "modele_slug,structure_siret,contact_email,labels_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement,location_postal_code,diffusion_zone_type,is_contact_info_public"
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

        self.source_info = {
            "value": "file_name",
            "label": "Test Import",
        }

    def test_import_services_wet_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,"
        )
        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["geo_data_missing_lines"], [])

        self.assertEqual(created_service.structure, self.structure)
        self.assertEqual(created_service.model, self.service_model)
        self.assertEqual(created_service.contact_email, "referent@email.com")
        self.assertEqual(created_service.contact_name, "Test Person")
        self.assertEqual(created_service.contact_phone, "0123456789")
        self.assertEqual(created_service.diffusion_zone_type, "city")
        self.assertEqual(created_service.last_editor, self.importing_user)

        self.assertEqual(created_service.funding_labels.count(), 1)
        self.assertEqual(
            created_service.funding_labels.first().value, self.funding_label.value
        )
        self.assertFalse(created_service.is_contact_info_public)

    def test_import_services_dry_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=False
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["geo_data_missing_lines"], [])

        self.assertFalse(
            Service.objects.filter(contact_email="referent@email.com").exists()
        )

    def test_missing_siret(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},,referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0], "Ligne 2 : SIRET manquant pour la structure."
        )

    def test_invalid_structure_siret(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Structure avec le SIRET 'invalid-siret' introuvable.",
        )

    def test_invalid_service_model_slug(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid-slug,{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Modèle de service avec le slug invalid-slug introuvable.",
        )

    def test_missing_diffusion_zone_type(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.DRAFT)
        self.assertEqual(created_service.diffusion_zone_type, "")

    def test_invalid_diffusion_zone_type(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,{self.funding_label.value},,,,,,,,invalid_zone_type,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Type de zone de diffusion avec la valeur 'invalid_zone_type' introuvable.",
        )

    def test_invalid_funding_label(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,invalid-funding-label,,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Un ou plusieurs labels de financement sont introuvables : {'invalid-funding-label'}.",
        )

    def test_location_kinds(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,"a-distance,en-presentiel",,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.location_kinds.count(), 2)
        self.assertTrue(
            created_service.location_kinds.filter(label="En présentiel").exists()
        )
        self.assertTrue(
            created_service.location_kinds.filter(label="À distance").exists()
        )

    def test_invalid_location_kinds(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,invalid_kind,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Un ou plusieurs types d'accueil sont introuvables : {'invalid_kind'}.",
        )

    @patch(
        "dora.services.management.commands.import_services.get_geo_data",
        return_value=None,
    )
    def test_missing_geo_data(self, mock_geo_data):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["geo_data_missing_lines"]), 1)
        self.assertEqual(
            result["geo_data_missing_lines"][0],
            {
                "idx": 2,
                "address": "1 rue de test",
                "city": "Paris",
                "postal_code": "75020",
            },
        )

    @patch(
        "dora.services.management.commands.import_services.get_geo_data",
        return_value=GeoData(
            city_code=75020,
            city="Paris",
            postal_code="75020",
            address="1 rue de test",
            geom=Point(2.3522, 48.8566, srid=4326),
            lat="48.8566",
            lon="2.3522",
            score=1.0,
        ),
    )
    def test_valid_geo_data(self, mock_geo_data):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["geo_data_missing_lines"]), 0)
        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.city_code, "75020")
        self.assertEqual(
            created_service.geom,
            Point(2.3522, 48.8566, srid=4326),
        )
        self.assertEqual(created_service.diffusion_zone_details, "75020")

    def test_multiple_financing_labels(self):
        other_funding_label = baker.make(
            "FundingLabel", value="other-value", label="other-label"
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,"{self.funding_label.value},{other_funding_label.value}",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.funding_labels.count(), 2)
        self.assertTrue(
            created_service.funding_labels.filter(
                label=self.funding_label.label
            ).exists()
        )
        self.assertTrue(
            created_service.funding_labels.filter(
                label=other_funding_label.label
            ).exists()
        )

    def test_duplicated_financing_labels(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,"{self.funding_label.value},{self.funding_label.value}",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Ligne 2 : Un ou plusieurs labels de financement sont dupliqués.",
        )

    def test_handle_one_invalid_line(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid,{self.structure.siret},invalid@email.com,{self.funding_label.value},,,,,,,,,\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertFalse(
            Service.objects.filter(contact_email="invalid@email.com").exists()
        )
        self.assertEqual(result["created_count"], 0)
        self.assertEqual(len(result["errors"]), 1)

    def test_publish_eligible_remote_service(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,a-distance,,,,,city,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.PUBLISHED)

    def test_publish_eligible_in_person_service(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,en-presentiel,Paris,1 rue de test,,75020,city,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.PUBLISHED)

    def test_keep_in_person_service_in_draft_when_ineligible(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,en-presentiel,Paris,1 rue de test,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.DRAFT)

    def test_keep_service_in_draft_when_ineligible(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.DRAFT)

    def test_make_contact_info_public(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,oui"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])

        self.assertTrue(created_service.is_contact_info_public)

    def test_alert_duplicated_structure(self):
        baker.make(
            "Service",
            structure=self.structure,
            model=self.service_model,
            contact_email="referent@email.com",
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["duplicated_services"]), 1)
        self.assertEqual(
            result["duplicated_services"][0],
            f"Ligne 2 : Service dupliqué pour la structure {self.structure.siret} avec le modèle {self.service_model.slug} et le contact referent@email.com.",
        )

    def test_new_service_source(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader,
            self.importing_user,
            {"value": "new_file", "label": "new file used"},
            wet_run=True,
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])

        created_service = Service.objects.filter(creator=self.importing_user).last()

        new_source = ServiceSource.objects.get(value="new_file", label="new file used")

        self.assertEqual(created_service.source, new_source)

    def test_existing_service_source(self):
        existing_source = baker.make(
            "ServiceSource", value="existing_file", label="Existing File"
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader,
            self.importing_user,
            {"value": f"{existing_source.value}", "label": f"{existing_source.label}"},
            wet_run=True,
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])

        created_service = Service.objects.filter(creator=self.importing_user).last()
        self.assertEqual(created_service.source, existing_source)

    def test_invalid_headers(self):
        invalid_headers = "invalid_header,another_invalid_header"
        csv_content = (
            f"{invalid_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(
            reader,
            self.importing_user,
            {"value": "test", "label": "test"},
            wet_run=True,
        )

        self.assertEqual(result["created_count"], 0)
        self.assertIn(
            "En-têtes de colonnes invalides dans le fichier CSV :",
            result["errors"][0],
        )
        self.assertIn(
            "invalid_header",
            result["errors"][0],
        )
        self.assertIn(
            "another_invalid_header",
            result["errors"][0],
        )
