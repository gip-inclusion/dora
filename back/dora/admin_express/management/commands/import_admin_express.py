import os.path
import pathlib
import subprocess
import tempfile

from django.conf import settings
from django.contrib.gis.utils import LayerMapping
from django.db import connection
from django.db.models import F, Func, Value

from dora.admin_express.models import EPCI, City, Department, Region
from dora.admin_express.utils import normalize_string_for_search
from dora.core.commands import BaseCommand
from dora.core.utils import code_insee_to_code_dept

EXE_7ZR = "/app/.apt/usr/lib/p7zip/7zr" if not settings.DEBUG else "7zr"

# Using the fast OpenDataArchive mirror
# The original is at ftp://Admin_Express_ext:Dahnoh0eigheeFok@ftp3.ign.fr/ADMIN-EXPRESS-COG_3-0__SHP__FRA_WM_2021-05-19.7z
AE_COG_LINK = "http://files.opendatarchives.fr/professionnels.ign.fr/adminexpress/ADMIN-EXPRESS-COG_3-0__SHP__FRA_WM_2021-05-19.7z"
AE_COG_FILE = "ADMIN-EXPRESS-COG_3-0__SHP__FRA_WM_2021-05-19.7z"
USE_TEMP_DIR = not settings.DEBUG


def normalize_model(Model, with_dept=False):
    objects = Model.objects.all()
    for object in objects:
        object.normalized_name = normalize_string_for_search(object.name)
        if with_dept:
            object.normalized_name += f" {code_insee_to_code_dept(object.code)}"
    Model.objects.bulk_update(objects, ["normalized_name"], 1000)


class Command(BaseCommand):
    help = "Import the latest Admin Express COG database"

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

            shapefile_dir = (
                the_dir
                / "ADMIN-EXPRESS-COG_3-0__SHP__FRA_2021-05-19"
                / "ADMIN-EXPRESS-COG"
                / "1_DONNEES_LIVRAISON_2021-05-19"
                / "ADECOG_3-0_SHP_WGS84G_FRA"
            )
            # Communes
            shapefile = shapefile_dir / "COMMUNE.shp"
            mapping = {
                "code": "INSEE_COM",
                "name": "NOM",
                "department": "INSEE_DEP",
                "region": "INSEE_REG",
                "epci": "SIREN_EPCI",
                "population": "POPULATION",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing cities"))
            lm = LayerMapping(City, shapefile, mapping)
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(City, with_dept=True)
            self.stdout.write(self.style.SUCCESS("Done"))

            # EPCI
            shapefile = shapefile_dir / "EPCI.shp"
            mapping = {
                "code": "CODE_SIREN",
                "name": "NOM",
                "nature": "NATURE",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing EPCIs"))
            lm = LayerMapping(EPCI, shapefile, mapping)
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
            shapefile = shapefile_dir / "DEPARTEMENT.shp"
            mapping = {
                "code": "INSEE_DEP",
                "name": "NOM",
                "region": "INSEE_REG",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing Departments"))
            lm = LayerMapping(Department, shapefile, mapping)
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(Department)
            self.stdout.write(self.style.SUCCESS("Done"))

            # Regions
            shapefile = shapefile_dir / "REGION.shp"
            mapping = {
                "code": "INSEE_REG",
                "name": "NOM",
                "geom": "MULTIPOLYGON",
            }
            self.stdout.write(self.style.SUCCESS("Importing Regions"))
            lm = LayerMapping(Region, shapefile, mapping)
            lm.save(progress=True, strict=True)
            self.stdout.write(self.style.SUCCESS("Import successful"))
            self.stdout.write(self.style.SUCCESS("Normalizing…"))
            normalize_model(Region)
            self.stdout.write(self.style.SUCCESS("Done"))

        self.stdout.write(self.style.SUCCESS("VACUUM ANALYZE"))
        cursor = connection.cursor()
        cursor.execute("VACUUM ANALYZE")
