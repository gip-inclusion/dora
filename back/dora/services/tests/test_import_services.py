import csv
import io
from unittest import TestCase
from unittest.mock import patch

from django.contrib.gis.geos import Point
from model_bakery import baker

from dora.core.utils import GeoData
from dora.service_suggestions.tests import DUMMY_SUGGESTION
from dora.services.management.commands.import_services import import_services
from dora.services.models import Service


class ImportServicesTestCase(TestCase):
    def setUp(self):
        self.importing_user = baker.make("users.User")
        self.csv_headers = "modele_slug,structure_siret,contact_email,diffusion_zone_type,labels_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement,location_postal_code"
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
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},Test Person,0123456789,,,,,,"
        )
        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

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

    def test_import_services_dry_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=False)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(result["geo_data_missing_lines"], [])

        self.assertEqual(
            Service.objects.filter(contact_email="referent@email.com").count(), 0
        )

    def test_missing_siret(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},,referent@email.com,Commune,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0], "Erreur : SIRET manquant. Ligne 1 ignorée."
        )

    def test_invalid_structure_siret(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,Commune,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Erreur : Structure avec le SIRET 'invalid-siret' introuvable. Ligne 1 ignorée.",
        )

    def test_invalid_service_model_slug(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid-slug,{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "Erreur : Modèle de service avec le slug invalid-slug introuvable. Ligne 1 ignorée.",
        )

    def test_missing_diffusion_zone_type(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "Erreur : Type de zone de diffusion manquant. Ligne 1 ignorée.",
        )

    def test_invalid_diffusion_zone_type(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,invalid_zone_type,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Erreur lors du traitement de la ligne 1 - Type de zone de diffusion avec la valeur 'invalid_zone_type' introuvable. Valeur ignorée.",
        )

    def test_invalid_funding_label(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,invalid-funding-label,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "Erreur lors du traitement de la ligne 1 - Un ou plusieurs labels de financement sont introuvables : {'invalid-funding-label'}. Ligne ignorée.",
        )

    @patch(
        "dora.services.management.commands.import_services.get_geo_data",
        return_value=None,
    )
    def test_missing_geo_data(self, mock_geo_data):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,Paris,1 rue de test,,75020,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["geo_data_missing_lines"]), 1)
        self.assertEqual(
            result["geo_data_missing_lines"][0],
            {
                "idx": 1,
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
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,Paris,1 rue de test,,75020,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["geo_data_missing_lines"]), 0)
        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.city_code, "75020")
        self.assertEqual(
            created_service.geom,
            Point(2.3522, 48.8566, srid=4326),
        )
        self.assertEqual(created_service.diffusion_zone_details, "75020")

    def test_location_kinds(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,"a-distance,en-presentiel",,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

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
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,invalid_kind,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Erreur lors du traitement de la ligne 1 - Un ou plusieurs types d'accueil "
            "sont introuvables : {'invalid_kind'}. Ligne ignorée.",
        )

    def test_multiple_financing_labels(self):
        other_funding_label = baker.make(
            "FundingLabel", value="other-value", label="other-label"
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,"{self.funding_label.value},{other_funding_label.value}",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

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
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,"{self.funding_label.value},{self.funding_label.value}",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "Erreur lors du traitement de la ligne 1 - Un ou plusieurs labels de financement sont dupliqués. Ligne ignorée.",
        )

    def test_handle_one_invalid_line(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid,{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,,,,,\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,Commune,{self.funding_label.value},,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = import_services(reader, self.importing_user, wet_run=True)

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["errors"]), 1)
