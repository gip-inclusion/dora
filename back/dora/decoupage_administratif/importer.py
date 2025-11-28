import logging

from django.db import transaction

from .api_client import DecoupageAdministratifAPIClient
from .models import Commune, Departement, Epci, Region

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
                    "nom": region["nom"],
                },
            )

    @transaction.atomic
    def import_departements(self) -> None:
        payload = self.client.fetch_departements()
        for departement in payload:
            Departement.objects.update_or_create(
                code=departement["code"],
                defaults={
                    "nom": departement["nom"],
                    "code_region": departement["codeRegion"],
                },
            )

    @transaction.atomic
    def import_epci(self) -> None:
        payload = self.client.fetch_epci()
        for epci in payload:
            Epci.objects.update_or_create(
                code=epci["code"],
                defaults={
                    "nom": epci["nom"],
                    "codes_departements": epci.get("codesDepartements", []),
                    "codes_regions": epci.get("codesRegions", []),
                },
            )

    @transaction.atomic
    def import_communes(self) -> None:
        payload = self.client.fetch_communes()
        for commune in payload:
            Commune.objects.update_or_create(
                code=commune["code"],
                defaults={
                    "nom": commune["nom"],
                    "code_departement": commune.get("codeDepartement", ""),
                    "code_epci": commune.get("codeEpci", ""),
                    "code_region": commune.get("codeRegion", ""),
                    "codes_postaux": commune.get("codesPostaux", []),
                },
            )

    def import_all(self) -> None:
        """Importe toutes les entités dans l'ordre des dépendances."""
        self.import_regions()
        self.import_departements()
        self.import_epci()
        self.import_communes()
