import csv

from django.core.exceptions import ValidationError
from django.db import transaction

from dora.core.commands import BaseCommand
from dora.core.validators import validate_siret
from dora.structures.models import Structure, StructureNationalLabel


class Command(BaseCommand):
    help = "Assurer que uniquement les bonnes structures ont le label national Mob'In"

    def add_arguments(self, parser):
        parser.add_argument("filename", type=str)
        parser.add_argument(
            "--wet-run",
            action="store_true",
        )

    def handle(self, *args, **options):
        filename = options["filename"]
        wet_run = options["wet_run"]

        self.stdout.write("Production run" if wet_run else "Dry run")

        with open(filename) as f:
            reader = csv.reader(f)
            self.clean_mobin_label(reader, wet_run)

    MOBIN_LABEL = "mobin"

    HEADER = "Numéro de SIRET"

    def clean_mobin_label(self, reader, wet_run=False):
        try:
            mobin_label = StructureNationalLabel.objects.get(value=self.MOBIN_LABEL)
        except StructureNationalLabel.DoesNotExist:
            self.stderr.write("Le label Mob'in n'existe pas en base.")
            return

        structures_with_mobin_label = Structure.objects.filter(
            national_labels=mobin_label
        )

        ids_of_structures_with_label = structures_with_mobin_label.values_list(
            "id", flat=True
        )

        ids_of_eligible_structures = []
        total_labels_added = 0

        [headers, *lines] = reader

        if headers[0] != self.HEADER:
            self.stderr.write(f"Le CSV manque le header obligatioire {self.HEADER} !")
            return

        lines = [dict(zip(headers, line)) for line in lines]

        with transaction.atomic():
            sirets_from_csv = [row[self.HEADER] for row in lines]

            structures_in_csv = Structure.objects.filter(siret__in=sirets_from_csv)

            structures_in_csv_by_siret = {s.siret: s for s in structures_in_csv}

            for index, row in enumerate(lines, 2):
                siret = row[self.HEADER]
                try:
                    validate_siret(siret)

                    if not structures_with_mobin_label.filter(siret=siret).exists():
                        structure = structures_in_csv_by_siret.get(siret)

                        if not structure:
                            raise Structure.DoesNotExist

                        structure.national_labels.add(mobin_label)
                        self.stdout.write(
                            f"Ajouté le label à la structure dont le siret est {siret}"
                        )
                        total_labels_added += 1

                    else:
                        structure = structures_with_mobin_label.get(siret=siret)

                    ids_of_eligible_structures.append(structure.id)

                except ValidationError:
                    self.stderr.write(f"Erreur de validation du SIRET {index}: {siret}")
                except Structure.DoesNotExist:
                    self.stderr.write(f"Structure inexistant {index}: {siret}")
                except KeyError:
                    self.stderr.write(f"Erreur de format {index}: {siret}")
                except Structure.MultipleObjectsReturned:
                    self.stderr.write(f"Plusieurs structures avec le SIRET {siret}")
                except Exception as e:
                    self.stderr.write(f"Erreur inconnue {index}: {siret} - {e}")

            ids_of_ineligible_structures = set(ids_of_structures_with_label) - set(
                ids_of_eligible_structures
            )

            Structure.national_labels.through.objects.filter(
                structure_id__in=ids_of_ineligible_structures,
                structurenationallabel=mobin_label,
            ).delete()

            self.stdout.write(
                f"Mob'in a été enlevé de {len(ids_of_ineligible_structures)} structures"
            )
            self.stdout.write(f"Mob'in a été ajouté à {total_labels_added} structures")
            self.stdout.write(
                f"{len(ids_of_eligible_structures) - total_labels_added} structures ont déjà le label Mob'in"
            )

            if not wet_run:
                transaction.set_rollback(True)
