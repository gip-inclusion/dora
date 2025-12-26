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
# Inclut les données géographiques pour Saint-Martin (97801) dans la couche collectivite_territoriale
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

        self._import_saint_martin(gpkg_file)

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

    def _import_saint_martin(self, gpkg_file):
        if City.objects.filter(code="97801").exists():
            self.logger.warning("Saint-Martin (97801) existe déjà. Ignoré.")
            return

        self.logger.info("Import de Saint-Martin depuis collectivite_territoriale")

        ds = DataSource(gpkg_file)
        layer = ds["collectivite_territoriale"]

        saint_martin_feature = None
        for feature in layer:
            code_insee = feature.get("code_insee")
            nom = feature.get("nom_officiel")

            if code_insee == "978" or (nom and "Saint-Martin" in nom):
                saint_martin_feature = feature
                self.logger.info("Trouvé : %s (code : %s)", nom, code_insee)
                break

        if not saint_martin_feature:
            self.logger.warning(
                "Saint-Martin non trouvé dans la couche collectivite_territoriale"
            )
            return

        geom = saint_martin_feature.geom
        geom_geos = GEOSGeometry(geom.wkt, srid=geom.srid)

        official_name = saint_martin_feature.get("nom_officiel")
        region_code = saint_martin_feature.get("code_insee_de_la_region") or "NR"

        saint_martin = City(
            code="97801",  # Il faut utiliser le code insee de 5 chiffres
            name=official_name,
            department="978",
            region=region_code,
            geom=geom_geos,
            epci="NR",  # Pas disponible dans la layer collectivite_territoriale
            epcis=["NR"],
            population=31496,  # https://fr.wikipedia.org/wiki/Saint-Martin_(Antilles_fran%C3%A7aises)
        )
        saint_martin.normalized_name = normalize_string_for_search(saint_martin.name)
        saint_martin.normalized_name += f" {code_insee_to_code_dept(saint_martin.code)}"
        saint_martin.save()

        self.logger.info(
            "Import réussi : %s (code : %s)", saint_martin.name, saint_martin.code
        )

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
