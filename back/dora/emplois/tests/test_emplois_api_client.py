import httpx
import pytest
import respx

from dora.emplois import api_client
from dora.emplois.api_client import EmploisApiClient, EmploisAPIException

BASE_URL = "https://emplois.example.com"
ORIENTATIONS_URL = f"{BASE_URL}/api/v1/insertion/orientations"


@respx.mock
def test_fetch_received_orientations_single_page():
    orientation = {
        "created_at": "2026-07-27T15:09:18+02:00",
        "status": "VALIDÉE",
        "beneficiary_name": "Joe Blow",
        "france_travail_id": None,
        "service_uid": "dora--1907599a-42e6-4345-b115-d588cd075193",
        "sender_organization_name": "France Travail - ARLES",
        "sender_name": "Salma ABOUDI",
        "process_link": f"{BASE_URL}/insertion/orientations/process/?token=abc",
    }
    route = respx.post(ORIENTATIONS_URL).mock(
        return_value=httpx.Response(
            200, json={"count": 1, "next": None, "results": [orientation]}
        )
    )

    results = EmploisApiClient().fetch_received_orientations(structure_slug="slug")

    assert results == [orientation]

    request = route.calls.last.request
    assert request.url.params["page_size"] == str(api_client.PAGE_SIZE)
    assert b"structure_uid=slug" in request.content
    assert request.headers["Authorization"] == "Token token"


@respx.mock
def test_fetch_received_orientations_follows_next_pages():
    page_2_url = f"{ORIENTATIONS_URL}?page=2&page_size=100"
    page_3_url = f"{ORIENTATIONS_URL}?page=3&page_size=100"

    # Seul `beneficiary_name` est renseigné : il sert de marqueur pour vérifier
    # que les pages sont bien concaténées dans l'ordre.
    # Les routes sont évaluées dans l'ordre d'enregistrement : les pages
    # suivantes d'abord, sinon la première route les capterait aussi.
    respx.post(ORIENTATIONS_URL, params={"page": "3"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 3,
                "next": None,
                "results": [{"beneficiary_name": "Page 3"}],
            },
        )
    )
    respx.post(ORIENTATIONS_URL, params={"page": "2"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 3,
                "next": page_3_url,
                "results": [{"beneficiary_name": "Page 2"}],
            },
        )
    )
    respx.post(ORIENTATIONS_URL, params={"page_size": "100"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 3,
                "next": page_2_url,
                "results": [{"beneficiary_name": "Page 1"}],
            },
        )
    )

    results = EmploisApiClient().fetch_received_orientations(structure_slug="slug")

    assert [result["beneficiary_name"] for result in results] == [
        "Page 1",
        "Page 2",
        "Page 3",
    ]


@respx.mock
def test_fetch_received_orientations_sends_body_on_every_page():
    page_2 = respx.post(ORIENTATIONS_URL, params={"page": "2"}).mock(
        return_value=httpx.Response(
            200, json={"count": 2, "next": None, "results": [{"id": "page-2"}]}
        )
    )
    respx.post(ORIENTATIONS_URL, params={"page_size": "100"}).mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 2,
                "next": f"{ORIENTATIONS_URL}?page=2&page_size=100",
                "results": [{"id": "page-1"}],
            },
        )
    )

    EmploisApiClient().fetch_received_orientations(structure_slug="slug")

    assert b"structure_uid=slug" in page_2.calls.last.request.content


@respx.mock
def test_fetch_received_orientations_stops_after_max_pages(monkeypatch):
    monkeypatch.setattr(api_client, "MAX_PAGES", 2)
    route = respx.post(ORIENTATIONS_URL).mock(
        return_value=httpx.Response(
            200,
            json={
                "count": 99,
                # Une API qui renvoie toujours un « next » ne doit pas boucler.
                "next": f"{ORIENTATIONS_URL}?page=2&page_size=100",
                "results": [{"id": "random"}],
            },
        )
    )

    with pytest.raises(EmploisAPIException):
        EmploisApiClient().fetch_received_orientations(structure_slug="slug")

    assert route.call_count == 2


@respx.mock
@pytest.mark.parametrize(
    "response",
    [
        pytest.param(httpx.Response(500, json={"detail": "oups"}), id="http_500"),
        pytest.param(httpx.Response(200, text="<html>pas du json</html>"), id="html"),
        pytest.param(httpx.Response(200, json={"count": 0}), id="no_results_key"),
        pytest.param(httpx.Response(200, json=[]), id="list_payload"),
        pytest.param(httpx.Response(204), id="empty_body"),
    ],
)
def test_fetch_received_orientations_raises_on_unusable_response(response):
    respx.post(ORIENTATIONS_URL).mock(return_value=response)

    with pytest.raises(EmploisAPIException):
        EmploisApiClient().fetch_received_orientations(structure_slug="slug")


@respx.mock
def test_fetch_received_orientations_raises_on_connection_error():
    respx.post(ORIENTATIONS_URL).mock(side_effect=httpx.ConnectError("injoignable"))

    with pytest.raises(EmploisAPIException):
        EmploisApiClient().fetch_received_orientations(structure_slug="slug")
