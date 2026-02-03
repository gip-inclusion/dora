import logging
from typing import Any

import requests
from django.conf import settings

logger = logging.getLogger(__name__)


class DecoupageAdministratifAPIClient:
    """Client minimal pour interroger l'API de découpage administratif."""

    def __init__(
        self,
        *,
        base_url: str | None = None,
        timeout_seconds: int | None = None,
        session: requests.Session | None = None,
    ) -> None:
        self.base_url = (base_url or settings.GEO_API_GOUV_BASE_URL).rstrip("/")
        self.timeout_seconds = timeout_seconds or settings.GEO_API_GOUV_TIMEOUT_SECONDS
        self.session = session or requests.Session()

    def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        url = f"{self.base_url}{path}"
        logger.info("Fetching %s", url)
        response = self.session.get(url, params=params, timeout=self.timeout_seconds)
        response.raise_for_status()
        return response.json()

    def fetch_communes(self) -> list[dict[str, Any]]:
        return self._get(
            "/communes",
            params={
                "fields": ",".join(
                    [
                        "code",
                        "nom",
                        "codeDepartement",
                        "codeRegion",
                        "codesPostaux",
                        "codeEpci",
                        "population",
                        "centre",
                    ]
                ),
                "format": "json",
            },
        )

    def fetch_departements(self) -> list[dict[str, Any]]:
        return self._get(
            "/departements",
            params={"fields": "code,nom,codeRegion", "format": "json"},
        )

    def fetch_epci(self) -> list[dict[str, Any]]:
        return self._get(
            "/epcis",
            params={
                "fields": ",".join(
                    [
                        "code",
                        "nom",
                        "codesDepartements",
                        "codesRegions",
                    ]
                ),
                "format": "json",
            },
        )

    def fetch_regions(self) -> list[dict[str, Any]]:
        return self._get(
            "/regions",
            params={"fields": "code,nom", "format": "json"},
        )
