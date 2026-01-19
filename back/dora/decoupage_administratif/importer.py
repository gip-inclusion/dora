import logging

from django.db import transaction

from .api_client import DecoupageAdministratifAPIClient
from .models import EPCI, City, Department, Region

logger = logging.getLogger(__name__)


class DecoupageAdministratifImporter:
    """Charge les données depuis l'API et les stocke en base."""

    def __init__(self, client: DecoupageAdministratifAPIClient | None = None) -> None:
        self.client = client or DecoupageAdministratifAPIClient()

    @transaction.atomic
    def import_regions(self) -> None:
        payload = self.client.fetch_regions()
        for region in payload:
            Region.objects.update_or_create(
                code=region["code"],
                defaults={
                    "name": region["nom"],
                },
            )

    @transaction.atomic
    def import_departements(self) -> None:
        payload = self.client.fetch_departements()
        for dept in payload:
            Department.objects.update_or_create(
                code=dept["code"],
                defaults={
                    "name": dept["nom"],
                    "region": dept["codeRegion"],
                },
            )

    @transaction.atomic
    def import_epci(self) -> None:
        payload = self.client.fetch_epci()
        for epci in payload:
            EPCI.objects.update_or_create(
                code=epci["code"],
                defaults={
                    "name": epci["nom"],
                    "departments": epci.get("codesDepartements", []),
                    "regions": epci.get("codesRegions", []),
                },
            )

    @transaction.atomic
    def import_communes(self) -> None:
        payload = self.client.fetch_communes()
        for commune in payload:
            City.objects.update_or_create(
                code=commune["code"],
                defaults={
                    "name": commune["nom"],
                    "department": commune.get("codeDepartement", ""),
                    "epci": commune.get("codeEpci", ""),
                    "region": commune.get("codeRegion", ""),
                    "postal_codes": commune.get("codesPostaux", []),
                },
            )

    def import_all(self) -> None:
        """Importe toutes les entités dans l'ordre des dépendances."""
        self.import_regions()
        self.import_departements()
        self.import_epci()
        self.import_communes()
