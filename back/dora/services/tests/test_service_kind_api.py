"""Écriture et exposition de `Service.kind`, et service des types depuis le référentiel DI."""

from data_inclusion.schema.v1 import TypeService
from django.core.cache import cache

from dora.core.test_utils import make_published_service, make_structure, make_user


def _published_service(api_client, **kwargs):
    user = make_user(is_valid=True)
    service = make_published_service(structure=make_structure(user=user), **kwargs)
    api_client.force_authenticate(user=user)
    return service


def test_service_detail_exposes_the_kind(api_client):
    service = _published_service(api_client, kind="atelier")

    response = api_client.get(f"/services/{service.slug}/")

    assert response.status_code == 200
    assert response.data["kind"] == "atelier"
    assert response.data["kind_display"] == "Atelier"


def test_service_without_kind_exposes_null(api_client):
    service = _published_service(api_client)

    response = api_client.get(f"/services/{service.slug}/")

    assert response.data["kind"] is None
    assert response.data["kind_display"] is None


def test_kind_is_writable(api_client):
    service = _published_service(api_client, kind="information")

    response = api_client.patch(f"/services/{service.slug}/", {"kind": "formation"})

    assert response.status_code == 200
    assert response.data["kind"] == "formation"
    service.refresh_from_db()
    assert service.kind == "formation"


def test_an_empty_kind_is_stored_as_null(api_client):
    service = _published_service(api_client, kind="information")

    response = api_client.patch(f"/services/{service.slug}/", {"kind": ""})

    assert response.status_code == 200
    service.refresh_from_db()
    assert service.kind is None


def test_an_unknown_kind_is_rejected(api_client):
    service = _published_service(api_client, kind="information")

    response = api_client.patch(f"/services/{service.slug}/", {"kind": "inconnu"})

    assert response.status_code == 400
    service.refresh_from_db()
    assert service.kind == "information"


def test_option_kinds_come_from_the_di_referential(api_client):
    cache.delete("options:anon")

    response = api_client.get("/services-options/")

    assert response.status_code == 200
    assert response.data["kinds"] == [
        {"value": t.value, "label": t.label}
        for t in sorted(TypeService, key=lambda t: t.label)
    ]
