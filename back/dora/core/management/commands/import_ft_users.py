import csv

from dora.core.commands import BaseCommand
from dora.core.csv_user_import import ImportUserHelper

"""
Import des conseillers et admins de agences FT :
    - fichiers aux format CSV en entrée : un pour les admins, l'autre pour les conseillers
    - format : safir,nom,prenom,email (email est optionnel)

Les adresses e-mail sont déduites à partir du nom / prénom (si absentes).
"""


class Command(BaseCommand):
    def __init__(self):
        self.import_helper = ImportUserHelper()

    help = "Importe des administrateurs ou conseillers d'agence France Travail"

    def add_arguments(self, parser):
        parser.add_argument("filename")

        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Traitement *réel* du fichier d'entrée : ajout d'utilisateurs et envois d'e-mails",
        )
        parser.add_argument(
            "--admin",
            action="store_true",
            help="Crée des utilisateurs avec le statut d'aministrateur de structure",
        )

    def handle(self, *args, **options):
        filename = options["filename"]
        wet_run = options["wet_run"]
        admin = options["admin"]

        with open(filename) as structures_file:
            reader = csv.reader(structures_file)
            self.import_helper.import_france_travail_users(
                reader, wet_run=wet_run, make_users_admin=admin
            )
