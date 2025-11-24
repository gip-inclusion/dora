from __future__ import annotations

from typing import Callable

from django.core.management.base import BaseCommand

from dora.decoupage_administratif.importer import DecoupageAdministratifImporter


class Command(BaseCommand):
    help = "Importe les communes, départements, EPCI et régions depuis l'API de découpage administratif."

    def add_arguments(self, parser) -> None:
        parser.add_argument(
            "--scope",
            choices=["all", "regions", "departements", "epci", "communes"],
            default="all",
            help="Permet de restreindre l'import à un type d'entité (par défaut: all).",
        )

    def handle(self, *args, **options) -> None:
        scope: str = options["scope"]
        importer = DecoupageAdministratifImporter()
        actions: dict[str, Callable[[], None]] = {
            "all": importer.import_all,
            "regions": importer.import_regions,
            "departements": importer.import_departements,
            "epci": importer.import_epci,
            "communes": importer.import_communes,
        }

        self.stdout.write(self.style.NOTICE(f"Démarrage de l'import '{scope}'..."))
        actions[scope]()
        self.stdout.write(self.style.SUCCESS("Import terminé."))
