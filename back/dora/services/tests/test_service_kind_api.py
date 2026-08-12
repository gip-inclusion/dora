"""Écriture et exposition de `Service.kind`, et service des types depuis le référentiel DI."""

from data_inclusion.schema.v1 import TypeService
from django.core.cache import cache

from dora.core.test_utils import make_published_service, make_structure, make_user
from dora.services.models import ServiceKind


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
    # tolérance transitoire, en lecture cette fois : `kinds` reste servie, dérivée de `kind`
    assert response.data["kinds"] == ["atelier"]
    assert response.data["kinds_display"] == ["Atelier"]


def test_service_without_kind_exposes_null(api_client):
    service = _published_service(api_client)

    response = api_client.get(f"/services/{service.slug}/")

    assert response.data["kind"] is None
    assert response.data["kind_display"] is None
    assert response.data["kinds"] == []
    assert response.data["kinds_display"] == []


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


def test_a_front_still_sending_kinds_keeps_the_highest_priority_one(api_client):
    """Tolérance transitoire : front et back ne sont pas déployés au même instant."""
    service = _published_service(api_client)

    response = api_client.patch(
        f"/services/{service.slug}/", {"kinds": ["information", "aide-financiere"]}
    )

    assert response.status_code == 200
    assert response.data["kind"] == "aide-financiere"
    service.refresh_from_db()
    assert service.kind == "aide-financiere"


def test_kind_wins_over_kinds_when_both_are_sent(api_client):
    service = _published_service(api_client)

    response = api_client.patch(
        f"/services/{service.slug}/",
        {"kind": "atelier", "kinds": ["aide-financiere"]},
    )

    assert response.status_code == 200
    service.refresh_from_db()
    assert service.kind == "atelier"


def test_the_m2m_is_left_untouched(api_client):
    """`kinds` est gelée jusqu'à sa suppression : elle n'est plus ni lue ni écrite."""
    service = _published_service(api_client)
    service.kinds.set(ServiceKind.objects.filter(value="information"))

    response = api_client.patch(f"/services/{service.slug}/", {"kind": "atelier"})

    assert [k.value for k in service.kinds.all()] == ["information"]
    # y compris pour la compatibilité en lecture, qui dérive de `kind` et non de la M2M
    assert response.data["kinds"] == ["atelier"]


def test_option_kinds_come_from_the_di_referential(api_client):
    cache.delete("options:anon")
    # un type résiduel en base ne doit plus apparaître dans les options
    ServiceKind.objects.create(value="plus-utilise", label="Plus utilisé")

    response = api_client.get("/services-options/")

    assert response.status_code == 200
    assert response.data["kinds"] == [
        {"value": t.value, "label": t.label}
        for t in sorted(TypeService, key=lambda t: t.label)
    ]
