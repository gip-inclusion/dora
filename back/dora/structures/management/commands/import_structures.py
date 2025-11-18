import csv
import os

from dora.core.commands import BaseCommand
from dora.structures.csv_import import ImportStructuresHelper
from dora.users.models import User


class Command(BaseCommand):
    help = "Importe une liste de structures"

    def __init__(self, *args, **kwargs):
        self.import_structures_helper = ImportStructuresHelper()
        super().__init__(*args, **kwargs)

    def add_arguments(self, parser):
        parser.add_argument("file_path", help="Le path du fichier csv à importer")
        parser.add_argument(
            "-n",
            "--wet-run",
            action="store_true",
            help="Effectue l'opération de fichier et l'envoi de mail (mode 'dry-run' par défaut)",
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        wet_run = kwargs["wet_run"]

        bot_user = User.objects.get_dora_bot()

        with open(file_path, "r") as f:
            reader = csv.reader(f)
            file_name = os.path.basename(file_path).rsplit(".", 1)[0]
            service_source = {
                "value": file_name,
                "label": "Structures importés par la commande import_structures",
            }

            self.import_structures_helper.import_structures(
                reader,
                bot_user,
                service_source,
                wet_run,
            )
