import pytest

from dora.stats.models import PageView
from dora.stats.views import PATH_MAX_LENGTH, TITLE_MAX_LENGTH, USER_HASH_LENGTH

URL = "/stats/event/"


def test_pageview_truncates_long_path_and_title(api_client):
    payload = {
        "tag": "pageview",
        "path": "/" + "s" * PATH_MAX_LENGTH,
        "title": "t" * (TITLE_MAX_LENGTH + 1),
        "userHash": "a" * USER_HASH_LENGTH,
    }

    response = api_client.post(URL, data=payload)

    assert response.status_code == 201, response.data
    page_view = PageView.objects.get(id=response.data["event"])
    assert page_view.path == payload["path"][:PATH_MAX_LENGTH]
    assert page_view.title == "t" * TITLE_MAX_LENGTH


@pytest.mark.parametrize(
    "user_hash",
    [
        "a" * (USER_HASH_LENGTH + 1),
        "a" * (USER_HASH_LENGTH - 1),
        "-1' OR 5*5=25 -- ",
        1234,
        None,
    ],
)
def test_pageview_rejects_invalid_user_hash(api_client, user_hash):
    payload = {"tag": "pageview", "path": "/", "title": "", "userHash": user_hash}

    response = api_client.post(URL, data=payload, format="json")

    assert response.status_code == 400
    assert not PageView.objects.exists()


def test_event_without_user_hash_is_rejected(api_client):
    payload = {"tag": "pageview", "path": "/", "title": ""}

    response = api_client.post(URL, data=payload, format="json")

    assert response.status_code == 400
    assert not PageView.objects.exists()


@pytest.mark.parametrize(
    "invalid",
    [
        {"path": 123},
        {"path": {"a": 1}},
        {"path": ["x"]},
        {"path": None},
        {"title": 123},
        {"title": {"a": 1}},
        {"title": ["x"]},
    ],
)
def test_pageview_rejects_non_string_path_or_title(api_client, invalid):
    payload = {
        "tag": "pageview",
        "path": "/",
        "title": "",
        "userHash": "a" * USER_HASH_LENGTH,
        **invalid,
    }

    response = api_client.post(URL, data=payload, format="json")

    assert response.status_code == 400
    assert not PageView.objects.exists()


@pytest.mark.parametrize("title", [{}, {"title": None}])
def test_pageview_accepts_missing_title(api_client, title):
    payload = {
        "tag": "pageview",
        "path": "/",
        "userHash": "a" * USER_HASH_LENGTH,
        **title,
    }

    response = api_client.post(URL, data=payload, format="json")

    assert response.status_code == 201, response.data
    page_view = PageView.objects.get(id=response.data["event"])
    assert page_view.title == ""
