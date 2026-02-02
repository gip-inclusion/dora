import logging

from django.contrib.gis.geos import Point
from django.db import transaction

from dora.core.constants import WGS84
from dora.core.utils import code_insee_to_code_dept
from dora.decoupage_administratif.utils import normalize_string_for_search

from .api_client import DecoupageAdministratifAPIClient
from .models import EPCI, City, Department, Region

logger = logging.getLogger(__name__)


def _parse_center(center_data: dict | None) -> Point | None:
    """Parse le champ centre de l'API en Point PostGIS."""
    if not center_data or center_data.get("type") != "Point":
        return None
    coords = center_data.get("coordinates")
    if not coords or len(coords) != 2:
        return None
    return Point(coords[0], coords[1], srid=WGS84)


class DecoupageAdministratifImporter:
    """Charge les données depuis l'API et les stocke en base."""

    def __init__(self, client: DecoupageAdministratifAPIClient | None = None) -> None:
        self.client = client or DecoupageAdministratifAPIClient()

    @transaction.atomic
    def import_regions(self) -> None:
        payload = self.client.fetch_regions()
        for region in payload:
            name = region["nom"]
            Region.objects.update_or_create(
                code=region["code"],
                defaults={
                    "name": name,
                    "normalized_name": normalize_string_for_search(name),
                },
            )

    @transaction.atomic
    def import_departements(self) -> None:
        payload = self.client.fetch_departements()
        for dept in payload:
            name = dept["nom"]
            Department.objects.update_or_create(
                code=dept["code"],
                defaults={
                    "name": name,
                    "region": dept["codeRegion"],
                    "normalized_name": normalize_string_for_search(name),
                },
            )

    @transaction.atomic
    def import_epci(self) -> None:
        payload = self.client.fetch_epci()
        for epci in payload:
            name = epci["nom"]
            EPCI.objects.update_or_create(
                code=epci["code"],
                defaults={
                    "name": name,
                    "departments": epci.get("codesDepartements", []),
                    "regions": epci.get("codesRegions", []),
                    "normalized_name": normalize_string_for_search(name),
                },
            )

    @transaction.atomic
    def import_communes(self) -> None:
        payload = self.client.fetch_communes()
        for commune in payload:
            code = commune["code"]
            name = commune["nom"]
            normalized_name = normalize_string_for_search(name)
            normalized_name += f" {code_insee_to_code_dept(code)}"

            City.objects.update_or_create(
                code=code,
                defaults={
                    "name": name,
                    "department": commune.get("codeDepartement", ""),
                    "epci": commune.get("codeEpci", ""),
                    "region": commune.get("codeRegion", ""),
                    "postal_codes": commune.get("codesPostaux", []),
                    "population": commune.get("population", 0),
                    "center": _parse_center(commune.get("centre")),
                    "normalized_name": normalized_name,
                },
            )

    def import_all(self) -> None:
        """Importe toutes les entités dans l'ordre des dépendances."""
        self.import_regions()
        self.import_departements()
        self.import_epci()
        self.import_communes()
