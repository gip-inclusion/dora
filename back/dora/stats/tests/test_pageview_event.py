import pytest

from dora.stats.models import PageView

URL = "/stats/event/"


def test_pageview_truncates_long_path_and_title(api_client):
    payload = {
        "tag": "pageview",
        "path": "/services/" + "s" * 400,
        "title": "t" * 400,
        "userHash": "a" * 32,
    }

    response = api_client.post(URL, data=payload)

    assert response.status_code == 201, response.data
    page_view = PageView.objects.get(id=response.data["event"])
    assert page_view.path == payload["path"][:255]
    assert page_view.title == "t" * 255


@pytest.mark.parametrize("user_hash", ["a" * 40, "a" * 10, 1234])
def test_pageview_ignores_invalid_user_hash(api_client, user_hash):
    payload = {"tag": "pageview", "path": "/", "title": "", "userHash": user_hash}

    response = api_client.post(URL, data=payload, format="json")

    assert response.status_code == 201, response.data
    page_view = PageView.objects.get(id=response.data["event"])
    assert page_view.anonymous_user_hash == ""
