import csv
from pathlib import Path

from data_inclusion.schema.v0 import TypologieStructure
from django.core.management.base import BaseCommand
from django.db import transaction

from dora.core.models import ModerationStatus
from dora.core.notify import send_moderation_notification
from dora.sirene.models import Establishment
from dora.structures.models import Structure, StructureNationalLabel, StructureSource
from dora.users.models import User

BOT_USER = User.objects.get_dora_bot()
SOURCE = StructureSource.objects.get(value="dr-dt-pole-emploi")
LABEL = StructureNationalLabel.objects.get(value="france-travail")


class Command(BaseCommand):
    help = "Importe les DG/DR/DT France Travail, ainsi que leur code SAFIR"

    def add_arguments(self, parser):
        parser.add_argument(
            "--file", help="Fichier à importer (si diffétent de `drdt.csv`)"
        )

    def finalize_structure(self, structure, safir):
        structure.code_safir_ft = safir
        structure.source = SOURCE
        structure.creator = BOT_USER
        structure.last_editor = BOT_USER
        structure.typology = TypologieStructure.FT.value
        try:
            structure.save()
        except Exception as ex:
            print(
                f"Erreur à la création de la structure SIRET:{structure.siret} / SAFIR: {safir} ({ex})"
            )
        else:
            structure.national_labels.add(LABEL)
            send_moderation_notification(
                structure,
                BOT_USER,
                "Structure créée à partir de l’import DR/DT France Travail",
                ModerationStatus.VALIDATED,
            )

    def create_structure(self, siret, name, safir):
        try:
            establishment = Establishment.objects.get(siret=siret)
        except Establishment.DoesNotExist:
            print(f"Code siret inconnu : {siret} for {name}")
            return

        structure = Structure.objects.create_from_establishment(establishment)
        self.finalize_structure(structure, safir)

    def create_branch(self, parent, name, safir):
        try:
            establishment = Establishment.objects.get(siret=parent.siret)
        except Establishment.DoesNotExist:
            print(f"Code siret inconnu : {parent.siret} for {name}")
            return
        structure = Structure.objects.create_from_establishment(
            establishment, parent=parent
        )
        structure.name = name
        self.finalize_structure(structure, safir)

    def handle(self, *args, **options):
        file = options["file"]

        with transaction.atomic(durable=True):
            if file:
                mapping_file_path = Path(file)
            else:
                mapping_file_path = (
                    Path(__file__).parent.parent.parent / "data" / "drdt.csv"
                )

            with open(mapping_file_path) as mapping_file:
                reader = csv.DictReader(mapping_file)
                rows = list(reader)
                struct_types = ["DG", "DR", "DT"]
                for struct_type in struct_types:
                    structs = [row for row in rows if row["type"] == struct_type]
                    for struct in structs:
                        name = struct["nom"]
                        safir = struct["safir"]
                        siret = struct["siret"]

                        if len(safir) != 5:
                            print(f"Safir incorrect pour {name} ({safir})")
                            continue
                        if not siret:
                            print(f"Siret manquant pour {name} ({safir})")
                            continue

                        # S'il existe une structure avec ce code safir, mais un siret different,
                        # il faut résoudre manuellement
                        if (
                            Structure.objects.filter(code_safir_ft=safir, parent=None)
                            .exclude(siret=siret)
                            .exists()
                        ):
                            print(
                                f"{name} : ce code SAFIR ({safir}) existe déjà, mais il est associé à un autre SIRET"
                            )
                            continue
                        try:
                            structure = Structure.objects.get(siret=siret)
                            # Si la structure n'a pas de safir, on l'assigne
                            if not structure.code_safir_ft:
                                structure.code_safir_ft = safir
                                structure.save()
                                continue

                            # Si on a déjà une structure avec les mêmes siret/safir, on ignore
                            if structure.code_safir_ft == safir:
                                continue

                            # S'il existe déjà une antenne avec le même safir,dont le parent à le même siret, on ignore
                            if Structure.objects.filter(
                                parent=structure, code_safir_ft=safir
                            ).exists():
                                continue

                            # Sinon il faut créer une antenne
                            self.create_branch(structure, name, safir)
                        except Structure.DoesNotExist:
                            self.create_structure(siret, name, safir)
