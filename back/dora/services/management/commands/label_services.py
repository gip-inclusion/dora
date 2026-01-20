import csv
import pathlib

from dora.core.commands import BaseCommand
from dora.services.label_services import LabelServicesHelper
from dora.users.models import User


class Command(BaseCommand):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.label_services_helper = LabelServicesHelper()

    help = "Labelliser des services à partir d'un fichier CSV"

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
            self.label_services_helper.label_services(
                csv.reader(f), User.objects.get_dora_bot(), wet_run=wet_run
            )
