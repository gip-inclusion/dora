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

# GPKG version with WGS84 coordinates (mainland France + most overseas)
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
    help = "Import the latest Admin Express COG database (GPKG format)"

    def handle(self, *args, **options):
        with tempfile.TemporaryDirectory() as tmp_dir_name:
            if USE_TEMP_DIR:
                the_dir = pathlib.Path(tmp_dir_name)
            else:
                the_dir = pathlib.Path("/tmp")
            self.stdout.write("Saving AE files to " + str(the_dir))

            compressed_AE_file = the_dir / AE_COG_FILE

            if not os.path.exists(compressed_AE_file):
                self.stdout.write(self.style.NOTICE("Downloading AE COG file"))
                subprocess.run(
                    ["curl", AE_COG_LINK, "-o", compressed_AE_file],
                    check=True,
                )

                self.stdout.write(self.style.NOTICE("Decompressing the AE COG"))
                subprocess.run(
                    [EXE_7ZR, "-bd", "x", compressed_AE_file, f"-o{the_dir}"],
                    check=True,
                )

            # Find the GPKG file
            gpkg_files = list(the_dir.glob("**/*.gpkg"))

            if not gpkg_files:
                self.stdout.write(self.style.ERROR("No GPKG file found!"))
                return

            gpkg_file = str(gpkg_files[0])
            self.stdout.write(f"Found GPKG: {gpkg_file}")

            # Communes from GPKG layer
            mapping = {
                "code": "code_insee",
                "name": "nom_officiel",
                "department": "code_insee_du_departement",
                "region": "code_insee_de_la_region",
                "epci": "codes_siren_des_epci",  # Note: plural, contains EPCI codes
                "population": "population",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing cities"))
            lm = LayerMapping(
                City,
                gpkg_file,
                mapping,
                layer="commune",  # GPKG layer name
                transform=False,  # Already in WGS84
            )
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(City, with_dept=True)
            self.stdout.write(self.style.SUCCESS("Done"))

            # EPCI
            mapping = {
                "code": "code_siren",
                "name": "nom_officiel",
                "nature": "nature",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing EPCIs"))
            lm = LayerMapping(
                EPCI,
                gpkg_file,
                mapping,
                layer="epci",
                transform=False,
            )
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(EPCI)

            self.stdout.write(self.style.SUCCESS("Linking to Cities"))
            City.objects.update(
                epcis=Func(F("epci"), Value("/"), function="string_to_array")
            )
            self.stdout.write(self.style.SUCCESS("Linking depts and regions"))
            for epci in EPCI.objects.all():
                cities = City.objects.filter(epcis__contains=[epci.code])
                epci.departments = list(set(c.department for c in cities))
                epci.regions = list(set(c.region for c in cities))
                epci.save()

            self.stdout.write(self.style.SUCCESS("Done"))

            # Departements
            mapping = {
                "code": "code_insee",
                "name": "nom_officiel",
                "region": "code_insee_de_la_region",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing Departments"))
            lm = LayerMapping(
                Department,
                gpkg_file,
                mapping,
                layer="departement",
                transform=False,
            )
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(Department)
            self.stdout.write(self.style.SUCCESS("Done"))

            # Regions
            mapping = {
                "code": "code_insee",
                "name": "nom_officiel",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing Regions"))
            lm = LayerMapping(
                Region,
                gpkg_file,
                mapping,
                layer="region",
                transform=False,
            )
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(Region)
            self.stdout.write(self.style.SUCCESS("Done"))

            # Import Saint-Martin from collectivite_territoriale layer
            self._import_saint_martin(gpkg_file)

        self.stdout.write(self.style.SUCCESS("VACUUM ANALYZE"))
        cursor = connection.cursor()
        cursor.execute("VACUUM ANALYZE")

    def _import_saint_martin(self, gpkg_file):
        if City.objects.filter(code="97801").exists():
            self.stdout.write(
                self.style.WARNING("Saint-Martin (97801) already exists. Skipping.")
            )
            return

        self.stdout.write(
            self.style.SUCCESS("Importing Saint-Martin from collectivite_territoriale")
        )

        try:
            ds = DataSource(gpkg_file)
            layer = ds["collectivite_territoriale"]

            saint_martin_feature = None
            for feature in layer:
                code_insee = feature.get("code_insee")
                nom = feature.get("nom_officiel")

                if code_insee == "978" or (nom and "Saint-Martin" in nom):
                    saint_martin_feature = feature
                    self.stdout.write(f"Found: {nom} (code: {code_insee})")
                    break

            if not saint_martin_feature:
                self.stdout.write(
                    self.style.WARNING(
                        "Saint-Martin not found in collectivite_territoriale layer"
                    )
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
            saint_martin.normalized_name = normalize_string_for_search(
                saint_martin.name
            )
            saint_martin.normalized_name += (
                f" {code_insee_to_code_dept(saint_martin.code)}"
            )
            saint_martin.save()

            self.stdout.write(
                self.style.SUCCESS(
                    f"Successfully imported: {saint_martin.name} (code: {saint_martin.code})"
                )
            )

        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Saint-Martin import failed: {e}"))
            import traceback

            traceback.print_exc()
