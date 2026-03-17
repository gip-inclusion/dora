import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_published_service


def test_services_api_requires_authentication(api_client):
    response = api_client.get(reverse("emplois:service-list"))

    assert response.status_code == 401


def test_services_api_requires_emplois_email(api_client):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse("emplois:service-list"))

    assert response.status_code == 403


def test_services_api_list(emplois_user, api_client, published_service):
    list_response = api_client.get(reverse("emplois:service-list"))
    assert list_response.status_code == 200
    assert len(list_response.data) == 1

    data = list_response.data[0]
    assert data["id"] == str(published_service.id)
    assert data["short_desc"] == published_service.short_desc


def test_services_api_detail(emplois_user, api_client, published_service):
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
def test_services_api_is_read_only(
    emplois_user, api_client, published_service, method, use_detail, data
):
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
    for _ in range(3):
        make_published_service()

    with django_assert_num_queries(11):
        response = api_client.get(reverse("emplois:service-list"))

    assert response.status_code == 200
    assert len(response.data) == 3


def test_services_api_detail_queries_are_bounded(
    emplois_user,
    api_client,
    django_assert_num_queries,
    published_service,
):
    with django_assert_num_queries(11):
        response = api_client.get(
            reverse("emplois:service-detail", kwargs={"pk": published_service.id})
        )

    assert response.status_code == 200


def test_disabled_dora_form_di_structures_api_requires_authentication(api_client):
    response = api_client.get(reverse("emplois:disabled-dora-form-di-structure-list"))

    assert response.status_code == 401


def test_disabled_dora_form_di_structures_api_requires_emplois_email(api_client):
    user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=user)

    response = api_client.get(reverse("emplois:disabled-dora-form-di-structure-list"))

    assert response.status_code == 403


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
