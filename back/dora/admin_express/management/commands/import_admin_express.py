import os.path
import pathlib
import subprocess
import tempfile

from django.conf import settings
from django.contrib.gis.gdal import DataSource
from django.contrib.gis.geos import GEOSGeometry
from django.contrib.gis.utils import LayerMapping
from django.db import connection
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
USE_TEMP_DIR = not settings.DEBUG


def normalize_model(Model, with_dept=False):
    objects = Model.objects.all()
    for object in objects:
        object.normalized_name = normalize_string_for_search(object.name)
        if with_dept:
            object.normalized_name += f" {code_insee_to_code_dept(object.code)}"
    Model.objects.bulk_update(objects, ["normalized_name"], 1000)


class Command(BaseCommand):
    help = "Importer la base de donnée d'Admin Express COG la plus récente dans le format GPKG."

    def handle(self, *args, **options):
        gpkg_file = self._get_gpkg_file()

        self._import_communes(gpkg_file)

        self._import_collectivites_territoriales(gpkg_file)

        self._import_epci(gpkg_file)

        self._import_departments(gpkg_file)

        self._import_regions(gpkg_file)

        self.logger.info("VACUUM ANALYZE")
        cursor = connection.cursor()
        cursor.execute("VACUUM ANALYZE")

    def _get_gpkg_file(self):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            if USE_TEMP_DIR:
                the_dir = pathlib.Path(tmp_dir_name)
            else:
                the_dir = pathlib.Path("/tmp")
            self.logger.info("Sauvegarde des fichiers AE dans %s", the_dir)

            compressed_AE_file = the_dir / AE_COG_FILE

            if not os.path.exists(compressed_AE_file):
                self.logger.info("Téléchargement du fichier AE COG")
                subprocess.run(
                    ["curl", AE_COG_LINK, "-o", compressed_AE_file],
                    check=True,
                )

                self.logger.info("Décompression du fichier AE COG")
                subprocess.run(
                    [EXE_7ZR, "-bd", "x", compressed_AE_file, f"-o{the_dir}"],
                    check=True,
                )

            gpkg_files = list(the_dir.glob("**/*.gpkg"))

            if not gpkg_files:
                self.logger.error("Aucun fichier GPKG trouvé !")
                return

            gpkg_file = str(gpkg_files[0])
            self.logger.info("GPKG trouvé : %s", gpkg_file)

            # Vérifier que le fichier existe et afficher sa taille
            gpkg_path = pathlib.Path(gpkg_file)
            if not gpkg_path.exists():
                self.logger.error("Le fichier GPKG n'existe pas : %s", gpkg_file)
                return

            file_size = gpkg_path.stat().st_size
            self.logger.info(
                "Taille du fichier GPKG : %d bytes (%.2f MB)",
                file_size,
                file_size / (1024 * 1024),
            )

            if file_size == 0:
                self.logger.error("Le fichier GPKG est vide !")
                return

            # Tester avec ogrinfo pour vérifier que GDAL peut lire le fichier
            try:
                result = subprocess.run(
                    ["ogrinfo", "-so", "-al", gpkg_file],
                    capture_output=True,
                    text=True,
                    timeout=30,
                )
                if result.returncode != 0:
                    self.logger.error("ogrinfo a échoué : %s", result.stderr)
                else:
                    self.logger.info("ogrinfo a réussi à lire le fichier GPKG")
            except subprocess.TimeoutExpired:
                self.logger.warning(
                    "ogrinfo timeout - le fichier est peut-être très volumineux"
                )
            except Exception as e:
                self.logger.error("Erreur lors de l'exécution de ogrinfo : %s", e)

            return gpkg_file

    def _import_communes(self, gpkg_file):
        mapping = {
            "code": "code_insee",
            "name": "nom_officiel",
            "department": "code_insee_du_departement",
            "region": "code_insee_de_la_region",
            "epci": "codes_siren_des_epci",  # Note: plural, contains EPCI codes
            "population": "population",
            "geom": "MULTIPOLYGON",
        }
        self.logger.info("Import des communes")
        lm = LayerMapping(
            City,
            gpkg_file,
            mapping,
            layer="commune",  # GPKG layer name
            transform=False,  # Already in WGS84
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
        for epci in EPCI.objects.all():
            cities = City.objects.filter(epcis__contains=[epci.code])
            epci.departments = list(set(c.department for c in cities))
            epci.regions = list(set(c.region for c in cities))
            epci.save()

        self.logger.info("Terminé")

    def _import_departments(self, gpkg_file):
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
