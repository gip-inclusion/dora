import functools
import logging
from datetime import timedelta
from typing import Optional

import furl
import requests
from django.conf import settings

logger = logging.getLogger(__name__)


def log_and_raise(resp: requests.Response, *args, **kwargs):
    try:
        resp.raise_for_status()
    except requests.HTTPError as err:
        logger.error(resp.json())
        raise err


def di_client_factory():
    return DataInclusionClient(
        base_url=settings.DATA_INCLUSION_URL,
        token=settings.DATA_INCLUSION_STREAM_API_KEY,
        timeout_seconds=settings.DATA_INCLUSION_TIMEOUT_SECONDS,
    )


# TODO: use tenacity ?


def log_conn_error(func):
    @functools.wraps(func)
    def _func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except requests.ConnectionError as err:
            logger.error(err)
            raise err

    return _func


class DataInclusionClient:
    def __init__(
        self, base_url: str, token: str, timeout_seconds: Optional[int] = None
    ) -> None:
        self.base_url = furl.furl(base_url)
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {token}"})
        self.session.hooks["response"] = [log_and_raise]
        self.timeout_timedelta = (
            timedelta(seconds=timeout_seconds)
            if timeout_seconds is not None
            else timedelta(seconds=2)
        )

    def _get(self, url: furl.furl):
        return self.session.get(url, timeout=self.timeout_timedelta.total_seconds())

    def _get_pages(self, url: furl.furl):
        page = 1
        data = []

        while True:
            next_url = url.copy().add({"page": page})
            response = self._get(next_url)
            response_data = response.json()
            data += response_data["items"]

            if len(response_data["items"]) > 0:
                page += 1
            else:
                return data

    @log_conn_error
    def list_services(self, source: Optional[str] = None) -> Optional[list[dict]]:
        url = self.base_url.copy()
        url = url / "services"

        if source is not None:
            url.args["source"] = source

        try:
            return self._get_pages(url)
        except requests.HTTPError:
            return None

    @log_conn_error
    def retrieve_service(
        self,
        source: str,
        id: str,
        user_agent: Optional[str] = None,
        user_hash: Optional[str] = None,
    ) -> Optional[dict]:
        url = self.base_url.copy()
        url = url / "services" / source / id

        if user_agent is not None:
            self.session.headers.update({"User-Agent": user_agent})

        if user_hash is not None:
            self.session.headers.update({"Anonymous-User-Hash": user_hash})

        try:
            response = self._get(url)
            return response.json()
        except requests.HTTPError:
            return None
        except requests.ReadTimeout:
            return None

    @log_conn_error
    def search_services(
        self,
        sources: Optional[list[str]] = None,
        score_qualite_minimum: Optional[float] = None,
        code_insee: Optional[str] = None,
        thematiques: Optional[list[str]] = None,
        types: Optional[list[str]] = None,
        frais: Optional[list[str]] = None,
        lat: Optional[float] = None,
        lon: Optional[float] = None,
    ) -> Optional[list[dict]]:
        url = self.base_url.copy()
        url = url / "search/services"

        if sources is not None:
            url.args["sources"] = sources

        if score_qualite_minimum is not None:
            url.args["score_qualite_minimum"] = score_qualite_minimum

        if settings.DATA_INCLUSION_EXCLUDE_DUPLICATES:
            url.args["exclure_doublons"] = "true"

        if code_insee is not None:
            url.args["code_insee"] = code_insee

        if thematiques is not None:
            url.args["thematiques"] = thematiques

        if types is not None:
            url.args["types"] = types

        if frais is not None:
            url.args["frais"] = frais

        if lat is not None:
            url.args["lat"] = lat
        if lon is not None:
            url.args["lon"] = lon

        try:
            return self._get_pages(url)
        except requests.HTTPError:
            return None
        except requests.ReadTimeout:
            return None
        except requests.RequestException as err:
            logger.error(err)
            return None
