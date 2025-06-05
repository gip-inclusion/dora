import csv

from django.core.management.base import BaseCommand

from scripts.import_services import import_services


class Command(BaseCommand):
    help = "Créer des nouveaux services basés sur des modèles pour des structures en utilisant des infos fournies par un CSV"

    def add_arguments(self, parser):
        parser.add_argument("--file", help="Fichier csv à importer ")
        parser.add_argument(
            "--wet-run",
            help="Exécute l'import en mode test (ne modifie pas la base de données)",
            default=False,
        )

    def handle(self, *args, **kwargs):
        file = kwargs["file"]
        wet_run = bool(kwargs["wet_run"])

        with open(file, "r") as f:
            reader = csv.reader(f)
            import_services(reader, wet_run)
