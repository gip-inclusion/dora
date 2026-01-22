import csv
import pathlib
import subprocess
import tempfile

from django.db import connection
from django.db.utils import DataError

from dora.core.commands import BaseCommand
from dora.sirene.models import Establishment

from ._backup import (
    analyze,
    bulk_add_establishments,
    bulk_add_legal_units,
    clean_tmp_tables,
    create_indexes,
    create_legal_units_index,
    create_legal_units_table,
    create_table,
    drop_table,
    get_legal_units_batch,
    rename_table,
)

# Documentation des variables SIRENE : https://www.sirene.fr/static-resources/htm/v_sommaire.htm
SIRENE_TABLE = "sirene_establishment"
TMP_TABLE = "_sirene_establishment_tmp"
BACKUP_TABLE = "_sirene_establishment_bak"
LEGAL_UNITS_TMP_TABLE = "_sirene_legal_units_tmp"

LEGAL_UNITS_FILE_URL = "https://object.files.data.gouv.fr/data-pipeline-open/siren/stock/StockUniteLegale_utf8.zip"
ESTABLISHMENTS_FILE_URL = (
    "https://files.data.gouv.fr/geo-sirene/last/StockEtablissementActif_utf8_geo.csv.gz"
)


def clean_spaces(string):
    return string.replace("  ", " ").strip()


def table_exists(table_name: str) -> bool:
    """Check if a table exists in the database."""
    with connection.cursor() as c:
        c.execute(
            "SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = %s)",
            [table_name],
        )
        return c.fetchone()[0]


class Command(BaseCommand):
    help = "Import de la dernière base SIRENE géolocalisée"

    def add_arguments(self, parser):
        parser.add_argument(
            "--import-units",
            action="store_true",
            help="Phase 1: Télécharge et importe les unités légales dans une table temporaire.",
        )

        parser.add_argument(
            "--import-estab",
            action="store_true",
            help="Phase 2: Télécharge et importe les établissements (nécessite --import-units d'abord).",
        )

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
            help="Effectue un ANALYZE sur la table SIRENE.",
        )

        parser.add_argument(
            "--clean",
            action="store_true",
            help="Efface les tables de travail temporaires en DB.",
        )

    def download_legal_units(self, tmp_dir: pathlib.Path) -> pathlib.Path:
        """Download and extract legal units file. Returns path to CSV."""
        zipped_file = tmp_dir / "StockUniteLegale_utf8.zip"

        self.logger.info("Téléchargement des 'unités légales' (entreprises mères)")
        subprocess.run(
            ["curl", "-L", LEGAL_UNITS_FILE_URL, "-o", zipped_file],
            check=True,
        )

        self.logger.info("Décompression fichier unités légales")
        subprocess.run(
            ["unzip", "-o", zipped_file, "-d", tmp_dir],
            check=True,
        )

        return tmp_dir / "StockUniteLegale_utf8.csv"

    def download_establishments(self, tmp_dir: pathlib.Path) -> pathlib.Path:
        """Download and extract establishments file. Returns path to CSV."""
        gzipped_file = tmp_dir / "StockEtablissementActif_utf8_geo.csv.gz"

        self.logger.info("Téléchargement des établissements")
        subprocess.run(
            ["curl", "-L", ESTABLISHMENTS_FILE_URL, "-o", gzipped_file],
            check=True,
        )

        self.logger.info("Décompression du fichier établissements")
        subprocess.run(
            ["gzip", "-dk", gzipped_file],
            check=True,
        )

        return tmp_dir / "StockEtablissementActif_utf8_geo.csv"

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
            self._handle_activate()
            return

        if options.get("rollback"):
            self._handle_rollback()
            return

        if options.get("analyze"):
            self._handle_analyze()
            return

        if options.get("clean"):
            self._handle_clean()
            return

        if options.get("import_units"):
            self._handle_import_units()
            return

        if options.get("import_estab"):
            self._handle_import_estab()
            return

        # No flag: run both import phases sequentially
        self.logger.warning("Exécution des deux phases d'import séquentiellement...")
        self._handle_import_units()
        self._handle_import_estab()

    def _handle_activate(self):
        """Activate the temp table as the production table."""
        self.logger.warning("Activation de la table de travail")

        if not table_exists(TMP_TABLE):
            self.logger.error(
                "La table %s n'existe pas. Exécutez d'abord --import-units puis --import-estab.",
                TMP_TABLE,
            )
            return

        # on sauvegarde la base de production
        self.logger.info(" > sauvegarde de la table actuelle")
        # suppression d'un backup existant
        clean_tmp_tables(BACKUP_TABLE)
        # backup de la table actuelle
        rename_table(SIRENE_TABLE, BACKUP_TABLE)

        # on renomme la table de travail
        self.logger.info(" > renommage de la table de travail")
        rename_table(TMP_TABLE, SIRENE_TABLE)

        self.logger.info("Activation terminée")

    def _handle_rollback(self):
        """Rollback to the backup table."""
        self.logger.warning("Activation de la table sauvegardée")

        if not table_exists(BACKUP_TABLE):
            self.logger.error("La table %s n'existe pas.", BACKUP_TABLE)
            return

        rename_table(SIRENE_TABLE, TMP_TABLE)
        rename_table(BACKUP_TABLE, SIRENE_TABLE)
        rename_table(TMP_TABLE, BACKUP_TABLE)

        self.logger.info("Rollback terminé")

    def _handle_analyze(self):
        """Run ANALYZE on the sirene table."""
        self.logger.warning("Analyse de la table %s en cours...", SIRENE_TABLE)
        analyze(SIRENE_TABLE)
        self.logger.info("Analyse terminée")

    def _handle_clean(self):
        """Drop all temporary tables."""
        self.logger.warning("Suppression des tables temporaires...")
        clean_tmp_tables(TMP_TABLE, BACKUP_TABLE, LEGAL_UNITS_TMP_TABLE)
        self.logger.info("Suppression terminée")

    def _handle_import_units(self):
        """Phase 1: Download and import legal units to temp table."""
        self.logger.warning("Phase 1: Import des unités légales")

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_dir = pathlib.Path(tmp_dir_name)

            # Download legal units file
            stock_file = self.download_legal_units(tmp_dir)

            # Create temp table
            self.logger.info(" > création de la table des unités légales...")
            create_legal_units_table(LEGAL_UNITS_TMP_TABLE)

            # Import legal units
            self.logger.info(" > import des unités légales dans la DB...")
            legal_units_batch_size = 10_000
            legal_units_batch = []
            legal_units_count = 0

            with open(stock_file) as units_file:
                legal_units_reader = csv.DictReader(units_file, delimiter=",")

                for i, row in enumerate(legal_units_reader):
                    if (i % 1_000_000) == 0:
                        self.logger.info(" > %s unités légales traitées...", f"{i:,}")
                    if row["etatAdministratifUniteLegale"] == "A":
                        # On ignore les unités légales fermées
                        siren = row["siren"][:9]
                        name = self.get_ul_name(row)[:255]
                        legal_units_batch.append((siren, name))
                        legal_units_count += 1

                        if len(legal_units_batch) >= legal_units_batch_size:
                            bulk_add_legal_units(
                                LEGAL_UNITS_TMP_TABLE, legal_units_batch
                            )
                            legal_units_batch = []

                # Commit remaining batch
                if legal_units_batch:
                    bulk_add_legal_units(LEGAL_UNITS_TMP_TABLE, legal_units_batch)

            self.logger.info(
                " > %s unités légales importées dans la DB", f"{legal_units_count:,}"
            )

            # Create index for fast lookups
            self.logger.info(" > création de l'index sur les unités légales...")
            create_legal_units_index(LEGAL_UNITS_TMP_TABLE)

        self.logger.info(
            "Phase 1 terminée. Exécutez maintenant --import-estab pour la phase 2."
        )

    def _handle_import_estab(self):
        """Phase 2: Download and import establishments using legal units table."""
        self.logger.warning("Phase 2: Import des établissements")

        # Check prerequisite
        if not table_exists(LEGAL_UNITS_TMP_TABLE):
            self.logger.error(
                "La table %s n'existe pas. Exécutez d'abord --import-units.",
                LEGAL_UNITS_TMP_TABLE,
            )
            return

        with tempfile.TemporaryDirectory() as tmp_dir_name:
            tmp_dir = pathlib.Path(tmp_dir_name)

            # Download establishments file
            estab_file = self.download_establishments(tmp_dir)

            # Create establishments temp table
            self.logger.info(" > création de la table de travail")
            create_table(TMP_TABLE)

            # Import establishments
            self.logger.info(" > import des établissements...")

            with open(estab_file) as establishment_file:
                reader = csv.DictReader(establishment_file, delimiter=",")

                self.logger.info(" > insertion des données dans la table temporaire...")

                batch_size = 5_000
                estab_batch = []
                processed_count = 0
                inserted_count = 0

                for row in reader:
                    estab_batch.append(row)

                    if len(estab_batch) >= batch_size:
                        inserted = self._process_establishment_batch(estab_batch)
                        inserted_count += inserted
                        processed_count += len(estab_batch)
                        estab_batch = []

                        if (processed_count % 100_000) == 0:
                            self.logger.info(
                                " > %s établissements traités, %s insérés...",
                                f"{processed_count:,}",
                                f"{inserted_count:,}",
                            )

                # Process remaining batch
                if estab_batch:
                    inserted = self._process_establishment_batch(estab_batch)
                    inserted_count += inserted
                    processed_count += len(estab_batch)

            self.logger.info(
                " > %s établissements traités, %s insérés",
                f"{processed_count:,}",
                f"{inserted_count:,}",
            )

            # Cleanup: drop legal units temp table
            self.logger.info(" > suppression de la table des unités légales...")
            drop_table(LEGAL_UNITS_TMP_TABLE)

            # Create indexes on establishments table
            self.logger.info(" > création des indexes")
            create_indexes(TMP_TABLE)

        self.logger.info(
            "Phase 2 terminée. Exécutez --activate pour activer la nouvelle table."
        )

    def _process_establishment_batch(self, estab_rows: list[dict]) -> int:
        """Process a batch of establishments with batch lookup for legal units.
        Returns the number of establishments inserted."""
        # Get unique SIRENs from this batch
        sirens = list({row["siren"] for row in estab_rows})

        # Batch lookup: get all legal unit names in one query
        legal_units = get_legal_units_batch(LEGAL_UNITS_TMP_TABLE, sirens)

        # Create establishments for rows with matching legal units
        establishments = []
        for row in estab_rows:
            try:
                siren = row["siren"]
                parent_name = legal_units.get(siren)
                if parent_name:
                    establishments.append(
                        self.create_establishment(siren, parent_name, row)
                    )
            except DataError as err:
                self.logger.error("%s", err)
                self.logger.error("%s", row)

        # Bulk insert
        if establishments:
            bulk_add_establishments(TMP_TABLE, establishments)

        return len(establishments)
