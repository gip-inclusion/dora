import csv
import io
from unittest import TestCase
from unittest.mock import patch

import pytest
from django.contrib.gis.geos import Point
from django.core.management import call_command
from freezegun import freeze_time
from model_bakery import baker

from dora.core.utils import GeoData
from dora.services.csv_import import ImportServicesHelper
from dora.services.enums import ServiceStatus
from dora.services.models import Service, ServiceSource
from dora.users.models import User


@pytest.mark.parametrize("wet_run", [True, False])
def test_management_command(caplog, capsys, tmp_path, snapshot, wet_run):
    structure = baker.make("Structure", siret="12345678901234")
    service_model = baker.make(
        "Service",
        is_model=True,
        slug="test-service-model",
        name="test-service",
        structure=structure,
    )
    funding_label = baker.make("FundingLabel", value="test-value", label="test-label")

    csv_file = tmp_path.joinpath("file_name.csv")
    csv_file.write_text(
        "\n".join(
            [
                "modele_slug,structure_siret,contact_email,labels_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement,location_postal_code,diffusion_zone_type,is_contact_info_public",
                f"{service_model.slug},{structure.siret},referent@email.com,{funding_label.value},Test Person,0123456789,,,,,,city,",
            ]
        )
    )

    assert not Service.objects.filter(creator=User.objects.get_dora_bot()).exists()
    command_args = [csv_file.as_posix()]
    if wet_run:
        command_args.append("--wet-run")
    call_command("import_services", *command_args)

    assert (
        Service.objects.filter(creator=User.objects.get_dora_bot()).exists() is wet_run
    )
    assert caplog.messages[-1].startswith(
        "Management command dora.services.management.commands.import_services succeeded in "
    )
    assert caplog.messages[:-1] == snapshot(name="logs")
    assert capsys.readouterr() == snapshot(name="output")


class ImportServicesTestCase(TestCase):
    def setUp(self):
        self.importing_user = baker.make("users.User")
        self.csv_headers = "modele_slug,structure_siret,contact_email,labels_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement,location_postal_code,diffusion_zone_type,is_contact_info_public"
        self.structure = baker.make("Structure", siret="12345678901234")

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
        self.import_services_helper = ImportServicesHelper()

        self.geo_data = GeoData(
            city_code="75056",
            city="Paris",
            postal_code="75020",
            address="1 rue de test",
            geom=Point(2.3522, 48.8566, srid=4326),
            lat="48.8566",
            lon="2.3522",
            score=1.0,
        )
        self.city = baker.make("admin_express.City", code="75056", epci="012345678")

    def test_import_services_wet_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,"
        )
        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(result["errors"][0], "[2] SIRET manquant pour la structure.")

    def test_invalid_structure_siret(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "[2] Structure avec le SIRET 'invalid-siret' introuvable.",
        )

    def test_invalid_service_model_slug(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid-slug,{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "[2] Modèle de service avec le slug invalid-slug introuvable.",
        )

    def test_missing_diffusion_zone_type(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "[2] Type de zone de diffusion avec la valeur 'invalid_zone_type' introuvable.",
        )

    def test_invalid_funding_label(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,invalid-funding-label,,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)

        self.assertEqual(
            result["errors"][0],
            "[2] Un ou plusieurs labels de financement sont introuvables : {'invalid-funding-label'}.",
        )

    def test_location_kinds(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,"a-distance,en-presentiel",,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "[2] Un ou plusieurs types d'accueil sont introuvables : {'invalid_kind'}.",
        )

    @patch(
        "dora.services.csv_import.get_geo_data",
        return_value=None,
    )
    def test_missing_geo_data(self, mock_geo_data):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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
        "dora.services.csv_import.get_geo_data",
    )
    def test_valid_geo_data(self, mock_geo_data):
        mock_geo_data.return_value = self.geo_data

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["geo_data_missing_lines"]), 0)
        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.city_code, self.city.code)
        self.assertEqual(
            created_service.geom,
            Point(2.3522, 48.8566, srid=4326),
        )
        self.assertEqual(created_service.diffusion_zone_details, self.city.code)

    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_diffusion_zone_details_when_service_for_department(self, mock_geo_data):
        mock_geo_data.return_value = self.geo_data

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,department,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.diffusion_zone_details, self.city.department)

    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_diffusion_zone_details_when_service_for_dom_tom_department(
        self, mock_geo_data
    ):
        mock_geo_data.return_value = GeoData(
            city_code="97123",
            city="Réunion",
            postal_code="97123",
            address="1 rue de test",
            geom=Point(2.3522, 48.8566, srid=4326),
            lat="48.8566",
            lon="2.3522",
            score=1.0,
        )
        dom_tom_city = baker.make("admin_express.City", code="97123")

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,department,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(
            created_service.diffusion_zone_details, dom_tom_city.department
        )

    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_diffusion_zone_details_when_city_code_requires_translation_to_insee(
        self, mock_geo_data
    ):
        mock_geo_data.return_value = GeoData(
            city_code="75120",
            city="Réunion",
            postal_code="75120",
            address="1 rue de test",
            geom=Point(2.3522, 48.8566, srid=4326),
            lat="48.8566",
            lon="2.3522",
            score=1.0,
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,department,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.diffusion_zone_details, self.city.department)

    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_diffusion_zone_details_when_service_for_region(self, mock_geo_data):
        mock_geo_data.return_value = self.geo_data

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,region,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.diffusion_zone_details, self.city.region)

    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_diffusion_zone_details_when_service_for_epci(self, mock_geo_data):
        mock_geo_data.return_value = self.geo_data

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,epci,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(created_service.diffusion_zone_details, self.city.epci)

    def test_multiple_financing_labels(self):
        other_funding_label = baker.make(
            "FundingLabel", value="other-value", label="other-label"
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,"{self.funding_label.value},{other_funding_label.value}",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            "[2] Un ou plusieurs labels de financement sont dupliqués.",
        )

    def test_handle_one_invalid_line(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"invalid,{self.structure.siret},invalid@email.com,{self.funding_label.value},,,,,,,,,\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertFalse(
            Service.objects.filter(contact_email="invalid@email.com").exists()
        )
        self.assertEqual(result["created_count"], 0)
        self.assertEqual(len(result["errors"]), 1)

    @freeze_time("2022-01-01")
    def test_publish_eligible_remote_service(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,a-distance,,,,,city,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.PUBLISHED)
        self.assertEqual(
            str(created_service.publication_date), "2022-01-01 00:00:00+00:00"
        )

    @freeze_time("2022-01-01")
    @patch(
        "dora.services.csv_import.get_geo_data",
    )
    def test_publish_eligible_in_person_service(self, mock_geo_data):
        mock_geo_data.return_value = self.geo_data

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,en-presentiel,Paris,1 rue de test,,75020,city,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.PUBLISHED)
        self.assertEqual(
            str(created_service.publication_date), "2022-01-01 00:00:00+00:00"
        )

    def test_keep_in_person_service_in_draft_when_ineligible(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,0123456789,en-presentiel,Paris,1 rue de test,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.DRAFT)
        self.assertIsNone(created_service.publication_date)

    def test_keep_service_in_draft_when_ineligible(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        created_service = Service.objects.filter(creator=self.importing_user).last()

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(created_service.status, ServiceStatus.DRAFT)
        self.assertIsNone(created_service.publication_date)

    def test_make_contact_info_public(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,oui"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])
        self.assertEqual(len(result["duplicated_services"]), 1)
        self.assertEqual(
            result["duplicated_services"][0],
            {
                "contact_email": "referent@email.com",
                "idx": 2,
                "model_slug": "test-service-model",
                "siret": "12345678901234",
            },
        )

    def test_block_duplicated_service(self):
        baker.make(
            "Service",
            structure=self.structure,
            model=self.service_model,
            contact_email="referent@email.com",
            address1="1 rue de test",
            postal_code="75020",
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,,Paris,1 rue de test,,75020,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 0)
        self.assertEqual(
            result["errors"][0],
            f'[2] Le même service avec le modèle "{self.service_model.slug}", le référent "referent@email.com" '
            f"et la même adresse existe déjà pour la structure "
            f'dont le Siret est "{self.structure.siret}".',
        )
        self.assertEqual(len(result["duplicated_services"]), 0)

    def test_new_service_source(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
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

        result = self.import_services_helper.import_services(
            reader,
            self.importing_user,
            {"value": f"{existing_source.value}", "label": f"{existing_source.label}"},
            wet_run=True,
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])

        created_service = Service.objects.filter(creator=self.importing_user).last()
        self.assertEqual(created_service.source, existing_source)

    def test_missing_headers(self):
        missing_headers = "modele_slug,structure_siret,contact_email,diffusion_zone_type,labels_financement,contact_name,contact_phone,location_kinds,location_city,location_address,location_complement"
        csv_content = (
            f"{missing_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,"
            f"{self.funding_label.value},Test Person,,a-distance,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader,
            self.importing_user,
            {"value": "test", "label": "test"},
            wet_run=True,
        )

        self.assertCountEqual(
            result["missing_headers"],
            [
                "location_postal_code",
                "is_contact_info_public",
            ],
        )

    def test_results_do_not_carry_over_between_runs(self):
        baker.make(
            "Service",
            model=self.service_model,
            structure=self.structure,
            contact_email="referent@email.com",
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,\n"
            f"{self.service_model.slug},'invalid-siret',referent@email.com,{self.funding_label.value},,,,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=False
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(len(result["duplicated_services"]), 1)
        self.assertEqual(len(result["draft_services_created"]), 1)

        reader_2 = csv.reader(io.StringIO(csv_content))

        result_2 = self.import_services_helper.import_services(
            reader_2, self.importing_user, self.source_info, wet_run=False
        )

        self.assertEqual(result_2["created_count"], 1)
        self.assertEqual(len(result_2["errors"]), 1)
        self.assertEqual(len(result_2["duplicated_services"]), 1)
        self.assertEqual(len(result_2["draft_services_created"]), 1)

    def test_non_unique_source_label_wet_run(self):
        baker.make("ServiceSource", value="test_file", label="Test Source")

        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,\n"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader,
            self.importing_user,
            {
                "value": "test_file",
                "label": "New Label",
            },
            wet_run=True,
        )

        self.assertEqual(
            result["errors"][0],
            'Le fichier nommé "test_file" a déjà un nom de source stocké dans le base de données. Veuillez refaire l\'import avec un nouveau nom de source.',
        )

    def test_source_label_not_created_dry_run(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,\n"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader,
            self.importing_user,
            {
                "value": "test_file",
                "label": "New Label",
            },
            wet_run=False,
        )

        self.assertFalse(result["errors"])
        self.assertEqual(result["created_count"], 1)
        self.assertFalse(ServiceSource.objects.filter(label="New Label").exists())

    def test_source_label_not_created_wet_run_with_errors(self):
        csv_content = (
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},,,invalid_kind,,,,,,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(len(result["errors"]), 1)
        self.assertEqual(result["created_count"], 0)
        self.assertFalse(ServiceSource.objects.filter(**self.source_info).exists())

    def test_should_remove_first_two_lines(self):
        csv_content = (
            f"Some random text that should be ignored\n"
            f"Another line that should be ignored\n"
            f"{self.csv_headers}\n"
            f"{self.service_model.slug},{self.structure.siret},referent@email.com,{self.funding_label.value},Test Person,0123456789,,,,,,city,"
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader,
            self.importing_user,
            {
                "value": "test_file",
                "label": "New Label",
            },
            wet_run=False,
            should_remove_first_two_lines=True,
        )

        self.assertEqual(result["created_count"], 1)
        self.assertEqual(result["errors"], [])

    def test_should_handle_trailing_comma_in_column_with_multiple_values(self):
        other_funding_label = baker.make(
            "FundingLabel", value="other-value", label="other-label"
        )

        csv_content = (
            f"{self.csv_headers}\n"
            f'{self.service_model.slug},{self.structure.siret},referent@email.com,"{self.funding_label.value},{other_funding_label.value},",,,,,,,,'
        )

        reader = csv.reader(io.StringIO(csv_content))

        result = self.import_services_helper.import_services(
            reader, self.importing_user, self.source_info, wet_run=True
        )

        self.assertEqual(result["created_count"], 1)
