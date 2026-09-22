import logging

import httpx
from django.conf import settings

logger = logging.getLogger(__name__)

PAGE_SIZE = 100
# Garde-fou : évite une boucle infinie si l'API renvoie toujours un « next ».
MAX_PAGES = 100


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
        """Toutes les orientations reçues, pagination comprise.

        La route est paginée : on suit le lien ``next`` renvoyé par l'API
        jusqu'à épuisement, plutôt que de recalculer les numéros de page à
        partir de ``count`` (l'API est libre de plafonner ``page_size``).
        """
        results = []
        url = "api/v1/insertion/orientations"
        # ``page`` et ``page_size`` sont lus dans la query string, pas dans le
        # corps de la requête, même pour un POST.
        params = {"page_size": PAGE_SIZE}

        for _ in range(MAX_PAGES):
            payload = self._payload(
                self.call(
                    "POST",
                    url,
                    data={"structure_uid": structure_slug},
                    params=params,
                )
            )
            results += payload["results"]

            next_url = payload.get("next")
            if not next_url:
                return results

            # ``next`` est une URL absolue qui porte déjà ``page`` et
            # ``page_size`` : inutile de les repasser.
            url, params = next_url, None

        raise EmploisAPIException(
            f"Pagination des orientations non terminée après {MAX_PAGES} pages."
        )

    def get_received_orientations_count(self, structure_slug: str) -> dict[str, int]:
        url = "api/v1/insertion/orientations-count"
        response = self.call("GET", url, params={"structure_uid": structure_slug})

        try:
            payload = response.json()
            return {
                "pending_count": int(payload["pending_count"]),
                "total_count": int(payload["total_count"]),
            }
        except (ValueError, KeyError, TypeError) as exc:
            logger.exception(
                "get_received_orientations_count des Emplois: réponse inattendue"
            )
            raise EmploisAPIException("Réponse inattendue des Emplois") from exc

    @staticmethod
    def _payload(response: httpx.Response) -> dict:
        try:
            payload = response.json()
            # Accès volontaire : une page sans « results » est une erreur.
            payload["results"]
        except (ValueError, KeyError, TypeError) as exc:
            logger.exception(
                "fetch_received_orientations des Emplois: réponse inattendue"
            )
            raise EmploisAPIException("Réponse inattendue des Emplois") from exc
        return payload
