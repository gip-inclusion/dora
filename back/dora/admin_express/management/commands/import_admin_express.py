import os.path
import pathlib
import subprocess

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.utils import LayerMapping
from django.db.models import F, Func, Value

from dora.admin_express.models import EPCI, City, Department, Region
from dora.admin_express.utils import normalize_string_for_search
from dora.core.commands import BaseCommand
from dora.core.utils import code_insee_to_code_dept

EXE_7ZR = "/app/.apt/usr/lib/p7zip/7zr" if not settings.DEBUG else "7zr"

# Version GPKG avec coordonnées WGS84 (France métropolitaine + DOM-TOM)
# Inclut les données géographiques pour Saint-Martin (97801) et Saint-Barthélemy(97701) dans la couche "collectivite_territoriale"
AE_COG_LINK = "https://data.geopf.fr/telechargement/download/ADMIN-EXPRESS-COG/ADMIN-EXPRESS-COG_4-0__GPKG_WGS84G_FRA_2025-01-01/ADMIN-EXPRESS-COG_4-0__GPKG_WGS84G_FRA_2025-01-01.7z"
AE_COG_FILE = "ADMIN-EXPRESS-COG_4-0__GPKG_WGS84G_FRA_2025-01-01.7z"
PERSISTENT_DIR = "/tmp/admin_express"


def normalize_model(Model, with_dept=False, batch_size=500):
    total = Model.objects.count()
    for offset in range(0, total, batch_size):
        objects = list(Model.objects.all().order_by("pk")[offset : offset + batch_size])
        for obj in objects:
            obj.normalized_name = normalize_string_for_search(obj.name)
            if with_dept:
                obj.normalized_name += f" {code_insee_to_code_dept(obj.code)}"
        Model.objects.bulk_update(objects, ["normalized_name"])


class Command(BaseCommand):
    help = "Importer la base de donnée d'Admin Express COG la plus récente dans le format GPKG."

    def add_arguments(self, parser):
        parser.add_argument(
            "--communes",
            action="store_true",
            help="Importer uniquement les communes",
        )
        parser.add_argument(
            "--collectivites",
            action="store_true",
            help="Importer uniquement les collectivités territoriales",
        )
        parser.add_argument(
            "--epci",
            action="store_true",
            help="Importer uniquement les EPCI",
        )
        parser.add_argument(
            "--departements",
            action="store_true",
            help="Importer uniquement les départements",
        )
        parser.add_argument(
            "--regions",
            action="store_true",
            help="Importer uniquement les régions",
        )

    def handle(self, *args, **options):
        run_all = not any(
            [
                options.get("communes"),
                options.get("collectivites"),
                options.get("epci"),
                options.get("departements"),
                options.get("regions"),
            ]
        )

        gpkg_file = self._get_gpkg_file()

        if not gpkg_file:
            return

        if run_all or options.get("communes"):
            self._import_communes(gpkg_file)

        if run_all or options.get("collectivites"):
            self._import_collectivites_territoriales(gpkg_file)

        if run_all or options.get("epci"):
            self._import_epci(gpkg_file)

        if run_all or options.get("departements"):
            self._import_departements(gpkg_file)

        if run_all or options.get("regions"):
            self._import_regions(gpkg_file)

    def _get_gpkg_file(self):
        the_dir = pathlib.Path(PERSISTENT_DIR)
        the_dir.mkdir(parents=True, exist_ok=True)
        self.logger.info("Sauvegarde des fichiers AE dans %s", the_dir)

        compressed_AE_file = the_dir / AE_COG_FILE

        gpkg_files = list(the_dir.glob("**/*.gpkg"))
        if gpkg_files:
            gpkg_file = str(gpkg_files[0])
            self.logger.info("GPKG déjà présent : %s", gpkg_file)
            return gpkg_file

        if not os.path.exists(compressed_AE_file):
            # Télécharger comme fichier temporaire pour assurer que le fichier est complèt
            temp_file = the_dir / f"{AE_COG_FILE}.tmp"
            try:
                self.logger.info("Téléchargement du fichier AE COG")
                subprocess.run(
                    ["curl", AE_COG_LINK, "-o", temp_file],
                    check=True,
                )
                # Renommer le fichier uniquement après le téléchargement réussit
                temp_file.rename(compressed_AE_file)
            except Exception:
                if temp_file.exists():
                    temp_file.unlink()
                raise

        self.logger.info("Décompression du fichier AE COG")
        subprocess.run(
            [EXE_7ZR, "-bd", "x", compressed_AE_file, f"-o{the_dir}"],
            check=True,
        )

        gpkg_files = list(the_dir.glob("**/*.gpkg"))

        if not gpkg_files:
            self.logger.error("Aucun fichier GPKG trouvé !")
            return None

        gpkg_file = str(gpkg_files[0])
        self.logger.info("GPKG trouvé : %s", gpkg_file)

        return gpkg_file

    def _import_communes(self, gpkg_file):
        mapping = {
            "code": "code_insee",
            "name": "nom_officiel",
            "department": "code_insee_du_departement",
            "region": "code_insee_de_la_region",
            "epci": "codes_siren_des_epci",
            "population": "population",
            "geom": "MULTIPOLYGON",
        }
        self.logger.info("Import des communes")
        lm = LayerMapping(
            City,
            gpkg_file,
            mapping,
            layer="commune",  # Le nom de la couche dans le fichier GPKG
            transform=False,  # Déjà dans le format WGS84
        )
        lm.save(progress=True, strict=True)
        self.logger.info("Import réussi")
        self.logger.info("Normalisation…")
        normalize_model(City, with_dept=True)
        self.logger.info("Terminé")

    def _import_collectivite_territoriale(
        self, gpkg_file, territory_name, city_code, department_code, population
    ):
        if City.objects.filter(code=city_code).exists():
            self.logger.warning(
                "%s (%s) existe déjà. Ignoré.", territory_name, city_code
            )
            return

        self.logger.info(
            "Import de %s depuis collectivite_territoriale", territory_name
        )

        ds = DataSource(gpkg_file)
        layer = ds["collectivite_territoriale"]

        target_feature = None
        for feature in layer:
            code_insee = feature.get("code_insee")
            nom = feature.get("nom_officiel")

            if code_insee == department_code or (nom and territory_name in nom):
                target_feature = feature
                self.logger.info("Trouvé : %s (code : %s)", nom, code_insee)
                break

        if not target_feature:
            self.logger.warning(
                "%s non trouvé dans la couche collectivite_territoriale", territory_name
            )
            return

        geom = target_feature.geom
        geom_geos = GEOSGeometry(geom.wkt, srid=geom.srid)

        official_name = target_feature.get("nom_officiel")
        region_code = target_feature.get("code_insee_de_la_region") or "NR"

        city = City(
            code=city_code,  # Il faut utiliser le code insee de 5 chiffres
            name=official_name,
            department=department_code,
            region=region_code,
            geom=geom_geos,
            epci="NR",  # Pas disponible dans la couche "collectivite_territoriale"
            epcis=["NR"],
            population=population,
        )
        city.normalized_name = normalize_string_for_search(city.name)
        city.normalized_name += f" {code_insee_to_code_dept(city.code)}"
        city.save()

        self.logger.info("Import réussi : %s (code : %s)", city.name, city.code)

    def _import_collectivites_territoriales(self, gpkg_file):
        collectivites_territoriales = [
            {
                "territory_name": "Saint-Martin",
                "city_code": "97801",
                "department_code": "978",
                "population": 31951,  # https://adresse.data.gouv.fr/carte-base-adresse-nationale?id=97801#18.086004_-63.062500_12.41
            },
            {
                "territory_name": "Saint-Barthélemy",
                "city_code": "97701",
                "department_code": "977",
                "population": 10656,  # https://adresse.data.gouv.fr/carte-base-adresse-nationale?id=97701#17.919505_-62.849500_12.57
            },
        ]

        for collectivite in collectivites_territoriales:
            self._import_collectivite_territoriale(gpkg_file, **collectivite)

    def _import_epci(self, gpkg_file):
        mapping = {
            "code": "code_siren",
            "name": "nom_officiel",
            "nature": "nature",
            "geom": "MULTIPOLYGON",
        }
        self.logger.info("Import des EPCI")
        lm = LayerMapping(
            EPCI,
            gpkg_file,
            mapping,
            layer="epci",
            transform=False,
        )
        lm.save(progress=True, strict=True)
        self.logger.info("Import réussi")
        self.logger.info("Normalisation…")
        normalize_model(EPCI)

        self.logger.info("Liaison aux communes")
        City.objects.update(
            epcis=Func(F("epci"), Value("/"), function="string_to_array")
        )
        self.logger.info("Liaison des départements et régions")
        epci_batch_size = 100
        epci_count = EPCI.objects.count()
        for offset in range(0, epci_count, epci_batch_size):
            epcis = EPCI.objects.all()[offset : offset + epci_batch_size]
            for epci in epcis:
                cities = City.objects.filter(epcis__contains=[epci.code])
                epci.departments = list(set(c.department for c in cities))
                epci.regions = list(set(c.region for c in cities))
                epci.save()

        self.logger.info("Terminé")

    def _import_departements(self, gpkg_file):
        mapping = {
            "code": "code_insee",
            "name": "nom_officiel",
            "region": "code_insee_de_la_region",
            "geom": "MULTIPOLYGON",
        }
        self.logger.info("Import des départements")
        lm = LayerMapping(
            Department,
            gpkg_file,
            mapping,
            layer="departement",
            transform=False,
        )
        lm.save(progress=True, strict=True)
        self.logger.info("Import réussi")
        self.logger.info("Normalisation…")
        normalize_model(Department)
        self.logger.info("Terminé")

    def _import_regions(self, gpkg_file):
        mapping = {
            "code": "code_insee",
            "name": "nom_officiel",
            "geom": "MULTIPOLYGON",
        }
        self.logger.info("Import des régions")
        lm = LayerMapping(
            Region,
            gpkg_file,
            mapping,
            layer="region",
            transform=False,
        )
        lm.save(progress=True, strict=True)
        self.logger.info("Import réussi")
        self.logger.info("Normalisation…")
        normalize_model(Region)
        self.logger.info("Terminé")
