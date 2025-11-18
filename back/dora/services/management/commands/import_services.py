import csv
import os

from dora.core.commands import BaseCommand
from dora.services.csv_import import ImportServicesHelper
from dora.users.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.import_services_helper = ImportServicesHelper()

    help = "Créer des nouveaux services basés sur des modèles pour des structures en utilisant les infos fournies par un CSV"

    def add_arguments(self, parser):
        parser.add_argument("file_path", help="Le path du fichier csv à importer")
        parser.add_argument(
            "--wet-run",
            help="Exécuter l'import en vrai (modifie la base de données)",
            action="store_true",
        )

    def handle(self, *args, **kwargs):
        file_path = kwargs["file_path"]
        wet_run = bool(kwargs["wet_run"])
        bot_user = User.objects.get_dora_bot()

        with open(file_path, "r") as f:
            reader = csv.reader(f)
            file_name = os.path.basename(file_path).rsplit(".", 1)[0]
            service_source = {
                "value": file_name,
                "label": "Services importés par la commande import_services",
            }
            self.import_services_helper.import_services(
                reader, bot_user, service_source, wet_run
            )
