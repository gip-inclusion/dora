import pytest

from dora.stats.models import SearchView

URL = "/stats/event/"


@pytest.fixture
def base_payload():
    return {
        "tag": "search",
        "path": "/recherche-mots-cles",
        "userHash": "a" * 32,
        "searchNumResults": 12,
        "categoryIds": [],
        "subCategoryIds": [],
        "kinds": [],
        "feeConditions": [],
        "locationKinds": [],
    }


def post_search_view(api_client, payload):
    response = api_client.post(URL, data=payload)
    assert response.status_code == 201, response.data
    return SearchView.objects.get(id=response.data["event"])


@pytest.mark.parametrize(
    "location,expected",
    [
        pytest.param(
            {"searchCityCode": "33063", "searchDepartment": "", "searchRegion": ""},
            ("33063", "", ""),
            id="adresse-ou-commune",
        ),
        pytest.param(
            {"searchCityCode": "", "searchDepartment": "33", "searchRegion": ""},
            ("", "33", ""),
            id="departement",
        ),
        pytest.param(
            {"searchCityCode": "", "searchDepartment": "", "searchRegion": "75"},
            ("", "", "75"),
            id="region",
        ),
    ],
)
def test_keyword_search_stores_selected_location(
    api_client, base_payload, location, expected
):
    event = post_search_view(
        api_client,
        {**base_payload, "searchType": "mots_cles", "keyword": "mobilité", **location},
    )

    assert (event.city_code, event.department, event.region) == expected
    assert event.search_type == "mots_cles"
    assert event.keyword == "mobilité"


def test_keyword_search_does_not_derive_department_from_city_code(
    api_client, base_payload
):
    event = post_search_view(
        api_client,
        {
            **base_payload,
            "searchType": "mots_cles",
            "searchCityCode": "97411",
            "searchDepartment": "",
            "searchRegion": "",
        },
    )

    assert event.department == ""


@pytest.mark.parametrize(
    "city_code,expected_department",
    [("33063", "33"), ("97411", "974"), ("", "")],
)
def test_thematic_search_derives_department(
    api_client, base_payload, city_code, expected_department
):
    event = post_search_view(
        api_client,
        {**base_payload, "searchType": "thematique", "searchCityCode": city_code},
    )

    assert event.city_code == city_code
    assert event.department == expected_department
    assert event.region == ""
