"""
La consultation des services (fiche, liste, page structure, favoris) suit la même
règle d'exposition que l'API v2 / data·inclusion (`Service.objects.filter_for_DI`),
sauf pour les ayants droit (staff, gestionnaire du département, membres).
"""

from datetime import timedelta

import pytest
from django.utils import timezone

from dora.core.test_utils import (
    make_published_service,
    make_structure,
    make_user,
)


@pytest.fixture
def suspended_service():
    return make_published_service(
        suspension_date=timezone.localdate() - timedelta(days=1)
    )


@pytest.fixture
def orphan_service():
    return make_published_service(structure=make_structure(department="31"))


@pytest.fixture
def outsider():
    return make_user()


def _get_service(api_client, service, user=None):
    if user:
        api_client.force_authenticate(user=user)
    return api_client.get(f"/services/{service.slug}/")


@pytest.mark.parametrize("authenticated", [False, True])
@pytest.mark.parametrize("service_fixture", ["suspended_service", "orphan_service"])
def test_non_exposed_service_is_not_visible(
    api_client, request, outsider, authenticated, service_fixture
):
    service = request.getfixturevalue(service_fixture)
    response = _get_service(api_client, service, outsider if authenticated else None)
    assert response.status_code == 404


@pytest.mark.parametrize("days", [0, 1])
def test_service_suspension_date_today_or_later_is_visible(api_client, days):
    service = make_published_service(
        suspension_date=timezone.localdate() + timedelta(days=days)
    )
    assert _get_service(api_client, service).status_code == 200


def test_member_can_see_its_suspended_service(api_client, suspended_service):
    member = make_user(structure=suspended_service.structure)
    assert _get_service(api_client, suspended_service, member).status_code == 200


def test_staff_can_see_orphan_structure_service(api_client, orphan_service):
    staff = make_user(is_staff=True)
    assert _get_service(api_client, orphan_service, staff).status_code == 200


def test_department_manager_can_see_orphan_structure_service(
    api_client, orphan_service
):
    manager = make_user(is_manager=True, departments=["31"])
    assert _get_service(api_client, orphan_service, manager).status_code == 200


def test_published_list_excludes_non_exposed_services(
    api_client, suspended_service, orphan_service
):
    exposed_service = make_published_service()
    response = api_client.get("/services/", {"published": "1"})
    slugs = {s["slug"] for s in response.data}
    assert slugs == {exposed_service.slug}


def test_structure_page_excludes_suspended_service(api_client, suspended_service):
    exposed_service = make_published_service(structure=suspended_service.structure)
    response = api_client.get(f"/structures/{suspended_service.structure.slug}/")
    slugs = {s["slug"] for s in response.data["services"]}
    assert slugs == {exposed_service.slug}
    assert response.data["num_services"] == 1


def test_member_counts_its_suspended_service(api_client, suspended_service):
    make_published_service(structure=suspended_service.structure)
    member = make_user(structure=suspended_service.structure)
    api_client.force_authenticate(user=member)
    response = api_client.get(f"/structures/{suspended_service.structure.slug}/")
    assert response.data["num_services"] == 2


def test_outsider_cant_bookmark_suspended_service(
    api_client, outsider, suspended_service
):
    api_client.force_authenticate(user=outsider)
    response = api_client.post("/bookmarks/", {"slug": suspended_service.slug})
    assert response.status_code == 403


def test_branch_card_counts_only_exposed_services(api_client):
    parent = make_structure(user=make_user())
    branch = make_structure(user=make_user(), parent=parent)
    make_published_service(structure=branch)
    make_published_service(
        structure=branch, suspension_date=timezone.localdate() - timedelta(days=1)
    )
    orphan_branch = make_structure(parent=parent)
    make_published_service(structure=orphan_branch)

    response = api_client.get(f"/structures/{parent.slug}/")
    counts = {b["slug"]: b["num_services"] for b in response.data["branches"]}
    assert counts == {branch.slug: 1, orphan_branch.slug: 0}


def test_branch_member_counts_its_suspended_service(api_client):
    parent = make_structure(user=make_user())
    member = make_user()
    branch = make_structure(user=member, parent=parent)
    make_published_service(structure=branch)
    make_published_service(
        structure=branch, suspension_date=timezone.localdate() - timedelta(days=1)
    )

    api_client.force_authenticate(user=member)
    response = api_client.get(f"/structures/{parent.slug}/")
    assert response.data["branches"][0]["num_services"] == 2


def test_active_structures_have_an_exposed_service(api_client):
    exposed_service = make_published_service()
    make_published_service(suspension_date=timezone.localdate() - timedelta(days=1))
    make_published_service(structure=make_structure())

    response = api_client.get("/structures/", {"active": "1"})
    slugs = {s["slug"] for s in response.data}
    assert slugs == {exposed_service.structure.slug}
