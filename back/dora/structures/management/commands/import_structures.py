import csv
import pathlib

from dora.core.commands import BaseCommand
from dora.structures.csv_import import ImportStructuresHelper
from dora.users.models import User


class Command(BaseCommand):
    help = "Importe une liste de structures"

    def __init__(self, *args, **kwargs):
        self.import_structures_helper = ImportStructuresHelper()
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", help="Le path du fichier csv à importer", type=pathlib.Path
        )
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Effectue l'opération de fichier et l'envoi de mail (mode 'dry-run' par défaut)",
        )

    def handle(self, file_path: pathlib.Path, wet_run, **options):
        with file_path.open() as f:
            self.import_structures_helper.import_structures(
                csv.reader(f),
                User.objects.get_dora_bot(),
                {
                    "value": file_path.stem,
                    "label": "Structures importés par la commande import_structures",
                },
                wet_run,
            )
