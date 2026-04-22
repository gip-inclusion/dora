import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_published_service
from dora.decoupage_administratif.models import AdminDivisionType, City
from dora.emplois.views import PREFETCH_RELATED_SERVICE_LIST
from dora.services.models import (
    BeneficiaryAccessMode,
    CoachOrientationMode,
    FundingLabel,
)


@pytest.mark.parametrize(
    "route_name",
    [
        "emplois:reference-data-list",
        "emplois:service-list",
        "emplois:disabled-dora-form-di-structure-list",
    ],
)
def test_api_requires_authentication(api_client, route_name):
    response = api_client.get(reverse(route_name))

    assert response.status_code == 401


@pytest.mark.parametrize(
    "route_name",
    [
        "emplois:reference-data-list",
        "emplois:service-list",
        "emplois:disabled-dora-form-di-structure-list",
    ],
)
def test_api_requires_emplois_email(api_client, route_name):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse(route_name))

    assert response.status_code == 403


@pytest.mark.parametrize(
    "method,data",
    [
        ("post", {"kind": "funding_label", "value": "v", "label": "l"}),
        ("delete", None),
    ],
    ids=["post", "delete"],
)
def test_reference_data_api_is_read_only(emplois_user, api_client, method, data):
    url = reverse("emplois:reference-data-list")
    client_method = getattr(api_client, method)
    response = client_method(url, data=data) if data is not None else client_method(url)

    assert response.status_code == 403


def test_reference_data_api_list(emplois_user, api_client):
    response = api_client.get(reverse("emplois:reference-data-list"))

    assert response.status_code == 200
    response_items = {
        (item["kind"], item["value"], item["label"]) for item in response.data
    }
    expected_items = {
        *{
            ("funding_label", item.value, item.label)
            for item in FundingLabel.objects.all()
        },
        *{
            ("beneficiary_access_mode", item.value, item.label)
            for item in BeneficiaryAccessMode.objects.all()
        },
        *{
            ("coach_orientation_mode", item.value, item.label)
            for item in CoachOrientationMode.objects.all()
        },
    }
    assert response_items == expected_items


def test_reference_data_api_list_queries_are_bounded(
    emplois_user, api_client, django_assert_num_queries
):
    with django_assert_num_queries(1):
        response = api_client.get(reverse("emplois:reference-data-list"))

    assert response.status_code == 200


def test_services_api_list(emplois_user, api_client):
    published_service = make_published_service()
    list_response = api_client.get(reverse("emplois:service-list"))
    assert list_response.status_code == 200
    assert len(list_response.data) == 1

    data = list_response.data[0]
    assert data["id"] == str(published_service.id)
    assert data["short_desc"] == published_service.short_desc


def test_services_api_detail(emplois_user, api_client):
    published_service = make_published_service()
    url = reverse("emplois:service-detail", kwargs={"pk": published_service.id})
    detail_response = api_client.get(url)
    assert detail_response.status_code == 200
    detail_data = detail_response.data
    assert detail_data["id"] == str(published_service.id)
    assert detail_data["short_desc"] == published_service.short_desc


@pytest.mark.parametrize(
    "method,use_detail,data",
    [
        ("post", False, {"name": "New service"}),
        ("patch", True, {"short_desc": "Updated"}),
        ("delete", True, None),
    ],
    ids=["post", "patch", "delete"],
)
def test_services_api_is_read_only(emplois_user, api_client, method, use_detail, data):
    published_service = make_published_service()
    if use_detail:
        url = reverse("emplois:service-detail", kwargs={"pk": published_service.id})
    else:
        url = reverse("emplois:service-list")
    client_method = getattr(api_client, method)
    response = client_method(url, data=data) if data is not None else client_method(url)

    assert response.status_code == 403


def test_services_api_list_queries_are_bounded(
    emplois_user,
    api_client,
    django_assert_num_queries,
):
    """
    Il faut assurer qu'il n'y a qu'un seul query pour toutes les villes
    """
    expected_query_count = len(PREFETCH_RELATED_SERVICE_LIST) + 1
    # +1 pour la requete de listing des services
    for i in range(5):
        city_code = f"7500{i}"
        baker.make(City, code=city_code, name="Paris")
        make_published_service(
            diffusion_zone_details=city_code, diffusion_zone_type=AdminDivisionType.CITY
        )

    with django_assert_num_queries(expected_query_count):
        response = api_client.get(reverse("emplois:service-list"))

    assert response.status_code == 200
    assert len(response.data) == 5


def test_services_api_detail_queries_are_bounded(
    emplois_user,
    api_client,
    django_assert_num_queries,
):
    published_service = make_published_service()
    with django_assert_num_queries(11):
        response = api_client.get(
            reverse("emplois:service-detail", kwargs={"pk": published_service.id})
        )

    assert response.status_code == 200


@pytest.mark.parametrize(
    "method,use_detail,data",
    [
        ("post", False, {"source": "foobar", "structure_id": "structure-1"}),
        ("patch", True, {"comment": "Commentaire"}),
        ("delete", True, None),
    ],
    ids=["post", "patch", "delete"],
)
def test_disabled_dora_form_di_structures_api_is_read_only(
    emplois_user,
    api_client,
    method,
    use_detail,
    data,
):
    item = baker.make("structures.DisabledDoraFormDIStructure")

    if use_detail:
        url = reverse(
            "emplois:disabled-dora-form-di-structure-detail", kwargs={"pk": item.id}
        )
    else:
        url = reverse("emplois:disabled-dora-form-di-structure-list")

    client_method = getattr(api_client, method)
    if data is not None:
        response = client_method(url, data=data)
    else:
        response = client_method(url)

    assert response.status_code == 403


def test_disabled_dora_form_di_structures_api_list(
    emplois_user, api_client, django_assert_num_queries
):
    baker.make("structures.DisabledDoraFormDIStructure", source="source-1")
    baker.make("structures.DisabledDoraFormDIStructure", source="source-2")

    api_client.force_authenticate(user=emplois_user)

    with django_assert_num_queries(1):
        response = api_client.get(
            reverse("emplois:disabled-dora-form-di-structure-list")
        )

    assert response.status_code == 200
    assert len(response.data) == 2


def test_disabled_dora_form_di_structures_api_detail(
    emplois_user, api_client, django_assert_num_queries
):
    api_client.force_authenticate(user=emplois_user)

    di_structure = baker.make(
        "structures.DisabledDoraFormDIStructure", source="source-1"
    )

    with django_assert_num_queries(1):
        response = api_client.get(
            reverse(
                "emplois:disabled-dora-form-di-structure-detail",
                kwargs={"pk": di_structure.id},
            )
        )

    assert response.status_code == 200
    assert response.data["source"] == "source-1"
    assert response.data["structure_id"] == di_structure.structure_id
