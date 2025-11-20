import csv
import os.path
import pathlib
import subprocess
import tempfile

from django.conf import settings
from django.db import transaction
from django.db.utils import DataError

from dora.core.commands import BaseCommand
from dora.sirene.models import Establishment

from ._backup import (
    bulk_add_establishments,
    clean_tmp_tables,
    create_indexes,
    create_table,
    rename_table,
    vacuum_analyze,
)

# Documentation des variables SIRENE : https://www.sirene.fr/static-resources/htm/v_sommaire.htm
USE_TEMP_DIR = not settings.DEBUG
SIRENE_TABLE = "sirene_establishment"
TMP_TABLE = "_sirene_establishment_tmp"
BACKUP_TABLE = "_sirene_establishment_bak"


def clean_spaces(string):
    return string.replace("  ", " ").strip()


def commit(rows):
    bulk_add_establishments(TMP_TABLE, rows)


class Command(BaseCommand):
    help = "Import de la dernière base SIRENE géolocalisée"

    def add_arguments(self, parser):
        parser.add_argument(
            "--activate",
            action="store_true",
            help="Active la table de travail temporaire générée par l'import.",
        )

        parser.add_argument(
            "--rollback",
            action="store_true",
            help="Active la table de travail sauvegardée en production.",
        )

        parser.add_argument(
            "--analyze",
            action="store_true",
            help="Effectue un VACUUM ANALYZE sur la base.",
        )

        parser.add_argument(
            "--clean",
            action="store_true",
            help="Efface les tables de travail temporaires en DB.",
        )

    def download_data(self, tmp_dir_name):
        if USE_TEMP_DIR:
            the_dir = pathlib.Path(tmp_dir_name)
        else:
            the_dir = pathlib.Path("/tmp")
        self.stdout.write("Sauvegarde des fichiers SIRENE dans : " + str(the_dir))

        legal_units_file_url = "https://object.files.data.gouv.fr/data-pipeline-open/siren/stock/StockUniteLegale_utf8.zip"
        zipped_stock_file = the_dir / "StockUniteLegale_utf8.zip"

        if not os.path.exists(zipped_stock_file):
            self.stdout.write(
                self.style.NOTICE(
                    "Téléchargement des 'unités légales' (entreprises mères)"
                )
            )
            subprocess.run(
                ["curl", legal_units_file_url, "-o", zipped_stock_file],
                check=True,
            )

            self.stdout.write(self.style.NOTICE("Décompression fichier unités légales"))
            subprocess.run(
                ["unzip", zipped_stock_file, "-d", the_dir],
                check=True,
            )

        stock_file = the_dir / "StockUniteLegale_utf8.csv"

        establishments_geo_file_url = "https://files.data.gouv.fr/geo-sirene/last/StockEtablissementActif_utf8_geo.csv.gz"
        gzipped_estab_file = the_dir / "StockEtablissementActif_utf8_geo.csv.gz"

        if not os.path.exists(gzipped_estab_file):
            self.stdout.write(self.style.NOTICE("Télécharchement des établissements"))
            subprocess.run(
                ["curl", establishments_geo_file_url, "-o", gzipped_estab_file],
                check=True,
            )

            self.stdout.write(
                self.style.NOTICE("Décompression du fichier établissements")
            )
            subprocess.run(
                ["gzip", "-dk", gzipped_estab_file],
                check=True,
            )

        estab_file = the_dir / "StockEtablissementActif_utf8_geo.csv"

        return stock_file, estab_file

    def get_ul_name(self, row):
        if row["categorieJuridiqueUniteLegale"] == "1000":
            # personne physique
            unit_name = row["denominationUsuelle1UniteLegale"] or (
                f"{row['prenomUsuelUniteLegale']} {row['nomUsageUniteLegale'] or row['nomUniteLegale']}"
            )
        else:
            # personne morale
            unit_name = (
                row["denominationUsuelle1UniteLegale"] or row["denominationUniteLegale"]
            )

            if row["sigleUniteLegale"]:
                unit_name += f" — {row['sigleUniteLegale']}"

        return unit_name

    def get_name(self, row):
        denom = row["denominationUsuelleEtablissement"]
        enseigne1 = (
            row["enseigne1Etablissement"]
            if row["enseigne1Etablissement"] != denom
            else ""
        )
        return clean_spaces(f"{denom} {enseigne1}")

    def get_address1(self, row):
        return clean_spaces(
            f"{row['numeroVoieEtablissement']} {row['indiceRepetitionEtablissement']} {row['typeVoieEtablissement']} {row['libelleVoieEtablissement']}"
        )

    def get_city_name(self, row):
        return clean_spaces(
            f"{row['libelleCedexEtablissement'] or row['libelleCommuneEtablissement']} {row['distributionSpecialeEtablissement']}"
        )

    def create_establishment(self, siren, parent_name, row):
        name = self.get_name(row)[:255]
        parent_name = parent_name[:255]
        full_search_text = f"{name} {parent_name}" if name != parent_name else name
        return Establishment(
            siren=siren[:9],
            siret=row["siret"][:14],
            name=name,
            parent_name=parent_name,
            address1=self.get_address1(row)[:255],
            address2=row["complementAdresseEtablissement"][:255],
            city=self.get_city_name(row)[:255],
            city_code=row["codeCommuneEtablissement"][:5],
            postal_code=(
                row["codeCedexEtablissement"] or row["codePostalEtablissement"]
            )[:5],
            ape=row["activitePrincipaleEtablissement"][:6],
            is_siege=row["etablissementSiege"] == "true",
            longitude=row["longitude"] if row["longitude"] else None,
            latitude=row["latitude"] if row["latitude"] else None,
            full_search_text=full_search_text,
        )

    def handle(self, *args, **options):
        if options.get("activate"):
            # activation de la table temporaire (si existante),
            # comme table de production (`sirene_establishment`)
            self.stdout.write(self.style.WARNING("Activation de la table de travail"))

            # on sauvegarde la base de production
            self.stdout.write(self.style.NOTICE(" > sauvegarde de la table actuelle"))
            # suppression d'un backup existant
            clean_tmp_tables(BACKUP_TABLE)
            # backup de la table actuelle
            rename_table(SIRENE_TABLE, BACKUP_TABLE)

            # on renomme la table de travail
            self.stdout.write(self.style.NOTICE(" > renommage de la table de travail"))
            rename_table(TMP_TABLE, SIRENE_TABLE)

            self.stdout.write(self.style.NOTICE("Activation terminée"))
            return

        if options.get("rollback"):
            # activation de la table sauvegardée
            self.stdout.write(self.style.WARNING("Activation de la table sauvegardée"))
            rename_table(SIRENE_TABLE, TMP_TABLE)
            rename_table(BACKUP_TABLE, SIRENE_TABLE)
            rename_table(TMP_TABLE, BACKUP_TABLE)

        if options.get("analyze"):
            # lance une analyse statistique sur la base Postgres
            self.stdout.write(self.style.WARNING("Analyse de la DB en cours..."))
            vacuum_analyze()
            self.stdout.write(self.style.NOTICE("Analyse terminée"))
            return

        if options.get("clean"):
            # Supprime les tables de travail / temporaires de la base Postgres
            self.stdout.write(
                self.style.WARNING("Suppression des tables temporaires...")
            )
            clean_tmp_tables(TMP_TABLE, BACKUP_TABLE)
            self.stdout.write(self.style.NOTICE("Suppression terminée"))
            return

        self.stdout.write(self.style.NOTICE(" > création de la base de travail"))
        # efface la précédente
        create_table(TMP_TABLE)

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            stock_file, estab_file = self.download_data(tmp_dir_name)

            num_stock_items = 0
            with open(stock_file) as f:
                num_stock_items = sum(1 for _ in f)

            legal_units = {}
            with open(stock_file) as units_file:
                legal_units_reader = csv.DictReader(units_file, delimiter=",")

                self.stdout.write(self.style.NOTICE("Parsing legal units"))

                for i, row in enumerate(legal_units_reader):
                    if (i % 1_000_000) == 0:
                        self.stdout.write(
                            self.style.NOTICE(
                                f"{round(100 * i / num_stock_items)}% done"
                            )
                        )
                    if row["etatAdministratifUniteLegale"] == "A":
                        # On ignore les unités légales fermées
                        legal_units[row["siren"]] = self.get_ul_name(row)

                self.stdout.write(
                    self.style.NOTICE(" > décompte des établissements...")
                )

                num_establishments = 0
                with open(estab_file) as f:
                    num_establishments = sum(1 for _ in f)
                last_prog = 0

                self.stdout.write(
                    self.style.NOTICE(f" > {num_establishments} établissements")
                )

            with open(estab_file) as establishment_file:
                self.stdout.write(self.style.NOTICE(" > import des établissements..."))
                reader = csv.DictReader(establishment_file, delimiter=",")

                with transaction.atomic(durable=True):
                    self.stdout.write(
                        self.style.WARNING(
                            " > insertion des données dans la table temporaire..."
                        )
                    )
                    # Establishment.objects.all().delete()
                    batch_size = 1_000
                    rows = []
                    for i, row in enumerate(reader):
                        if (i % batch_size) == 0:
                            prog = round(100 * i / num_establishments)
                            if prog != last_prog:
                                last_prog = prog
                            self.stdout.write(self.style.NOTICE(f"{prog}% done"))
                            commit(rows)
                            rows = []
                        try:
                            siren = row["siren"]
                            parent = legal_units.get(siren)
                            if parent:
                                rows.append(
                                    self.create_establishment(
                                        siren,
                                        parent,
                                        row,
                                    )
                                )

                        except DataError as err:
                            self.stdout.write(self.style.ERROR(err))
                            self.stdout.write(self.style.ERROR(row))

                    commit(rows)

                # recréation des indexes sur la table de travail
                self.stdout.write(self.style.NOTICE(" > re-création des indexes"))
                create_indexes(TMP_TABLE)

                # la sauvegarde de la base de production et l'analyse de la DB
                # ne sont pas automatique, voir arguments `--activate` et `--analyze`

                self.stdout.write(
                    self.style.SUCCESS(
                        "L'import est terminé. Ne pas oublier d'activer la table de travail (--activate)"
                    )
                )
