import csv

from django.core.management.base import BaseCommand

from dora.structures.csv_import import ImportStructuresHelper
from dora.users.models import User


class Command(BaseCommand):
    help = "Importe une liste de structures"

    def __init__(self, *args, **kwargs):
        self.bot_user = User.objects.get_dora_bot()
        self.source_info = {
            "value": "invitations-masse",
            "label": "Invitations en masse",
        }
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

    def handle(self, *args, **options):
        file_path = options["file_path"]
        wet_run = options["wet_run"]

        if wet_run:
            print("PRODUCTION RUN")
        else:
            print("DRY RUN")

        with open(file_path) as structures_file:
            reader = csv.DictReader(structures_file, delimiter=",")
            self.import_structures_helper.import_structures(
                reader,
                self.bot_user,
                self.source_info,
                wet_run,
            )
