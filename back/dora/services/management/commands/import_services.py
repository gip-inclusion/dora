import csv
import pathlib

from dora.core.commands import BaseCommand
from dora.services.csv_import import ImportServicesHelper
from dora.users.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_services_helper = ImportServicesHelper()

    help = "Créer des nouveaux services basés sur des modèles pour des structures en utilisant les infos fournies par un CSV"

    def add_arguments(self, parser):
        parser.add_argument(
            "file_path", help="Le path du fichier csv à importer", type=pathlib.Path
        )
        parser.add_argument(
            "--wet-run",
            help="Exécuter l'import en vrai (modifie la base de données)",
            action="store_true",
        )

    def handle(self, file_path: pathlib.Path, wet_run=False, **options):
        with file_path.open() as f:
            self.import_services_helper.import_services(
                csv.reader(f),
                User.objects.get_dora_bot(),
                {
                    "value": file_path.stem,
                    "label": "Services importés par la commande import_services",
                },
                wet_run,
            )
