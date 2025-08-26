import csv
import io

from rest_framework.test import APITestCase

from dora.core.test_utils import make_structure
from dora.structures.management.commands.clean_mobin_label import Command
from dora.structures.models import StructureNationalLabel


class CleanMobinLabelTestCase(APITestCase):
    def setUp(self):
        self.csv_header = "Numéro de SIRET"
        self.mobin_label, _ = StructureNationalLabel.objects.get_or_create(
            value="mobin"
        )
        self.structure_with_label = make_structure()
        self.structure_with_label.national_labels.add(self.mobin_label)

        self.structure_without_label = make_structure()

        self.command = Command()

    def test_apply_labels_to_correct_structures(self):
        csv_content = f"{self.csv_header}\n{self.structure_without_label.siret}"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=True)

        self.assertTrue(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertFalse(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_keep_label_when_eligible_structure_already_has_it(self):
        csv_content = f"{self.csv_header}\n{self.structure_with_label.siret}"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=True)

        self.assertTrue(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_handle_multiple_structures(self):
        structure_1 = make_structure()
        structure_2 = make_structure()

        csv_content = f"{self.csv_header}\n{self.structure_without_label.siret}\n{structure_1.siret}\n{structure_2.siret}"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=True)

        self.assertTrue(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertTrue(
            structure_1.national_labels.filter(id=self.mobin_label.id).exists()
        )
        self.assertTrue(
            structure_2.national_labels.filter(id=self.mobin_label.id).exists()
        )
        self.assertFalse(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_do_not_apply_labels_when_dry_run(self):
        csv_content = f"{self.csv_header}\n{self.structure_without_label.siret}"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=False)

        self.assertFalse(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertTrue(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_handle_mobin_label_not_found(self):
        self.mobin_label.value = "invalid"
        self.mobin_label.save()

        csv_content = f"{self.csv_header}\n{self.structure_without_label.siret}"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=False)

        self.assertFalse(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertTrue(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_handle_siret_invalid(self):
        csv_content = f"{self.csv_header}\ninvalid"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=False)

        self.assertFalse(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertTrue(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )

    def test_handle_siret_not_found(self):
        csv_content = f"{self.csv_header}\n01234567891234"
        reader = csv.reader(io.StringIO(csv_content))

        self.command.clean_mobin_label(reader, wet_run=False)

        self.assertFalse(
            self.structure_without_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
        self.assertTrue(
            self.structure_with_label.national_labels.filter(
                id=self.mobin_label.id
            ).exists()
        )
