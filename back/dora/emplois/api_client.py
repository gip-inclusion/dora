import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)


class EmploisAPIException(Exception):
    pass


class EmploisApiClient:
    def __init__(self):
        self.client = httpx.Client(
            base_url=settings.EMPLOIS_API_BASE_URL,
            headers={"Authorization": f"Token {settings.EMPLOIS_API_TOKEN}"},
        )

    def call(self, method: str, url: str, **kwargs) -> httpx.Response:
        try:
            response = self.client.request(method, url, **kwargs)
            response.raise_for_status()
        except httpx.HTTPError as exc:
            err_response = getattr(exc, "response", None)
            if err_response is None:
                error = str(exc)
            else:
                try:
                    error = err_response.json()
                except ValueError:
                    # Le corps n'est pas toujours du JSON (page d'erreur HTML…)
                    error = err_response.text
            logger.exception(
                "les emplois %s:%s error=%s",
                method,
                url,
                error,
            )
            raise EmploisAPIException(error) from exc

        return response

    def fetch_received_orientations(self, structure_slug: str) -> list[dict]:
        response = self.call(
            "POST",
            "api/v1/insertion/orientations",
            data={"structure_uid": structure_slug},
        )
        try:
            return response.json()["results"]
        except (ValueError, KeyError, TypeError) as exc:
            logger.exception(
                "fetch_received_orientations des Emplois: réponse inattendue"
            )
            raise EmploisAPIException("Réponse inattendue des Emplois") from exc
