"""Exposition en lecture de `Service.kind` et service des types depuis le référentiel DI."""

from data_inclusion.schema.v1 import TypeService
from django.core.cache import cache

from dora.core.test_utils import make_service, make_structure, make_user
from dora.services.enums import ServiceStatus
from dora.services.models import ServiceKind


def test_le_detail_dun_service_expose_kind(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user=user)
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    service.kinds.set(ServiceKind.objects.filter(value__in=["information", "atelier"]))
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/services/{service.slug}/")

    assert response.status_code == 200
    assert response.data["kind"] == "atelier"
    assert response.data["kind_display"] == "Atelier"
    # `kinds` reste exposé tant que le formulaire l'écrit
    assert sorted(response.data["kinds"]) == ["atelier", "information"]


def test_un_service_sans_type_expose_un_kind_vide(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user=user)
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    api_client.force_authenticate(user=user)

    response = api_client.get(f"/services/{service.slug}/")

    assert response.data["kind"] == ""
    assert response.data["kind_display"] == ""


def test_kind_est_en_lecture_seule(api_client):
    user = make_user(is_valid=True)
    structure = make_structure(user=user)
    service = make_service(structure=structure, status=ServiceStatus.PUBLISHED)
    service.kinds.set(ServiceKind.objects.filter(value="information"))
    api_client.force_authenticate(user=user)

    response = api_client.patch(f"/services/{service.slug}/", {"kind": "formation"})

    assert response.status_code == 200
    assert response.data["kind"] == "information"


def test_les_types_doptions_viennent_du_referentiel_di(api_client):
    cache.delete("options:anon")
    # un type résiduel en base ne doit plus apparaître dans les options
    ServiceKind.objects.create(value="plus-utilise", label="Plus utilisé")

    response = api_client.get("/services-options/")

    assert response.status_code == 200
    assert response.data["kinds"] == [
        {"value": t.value, "label": t.label}
        for t in sorted(TypeService, key=lambda t: t.label)
    ]
