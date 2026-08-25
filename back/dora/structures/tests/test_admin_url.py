import pytest
from django.test import override_settings

from dora.core.test_utils import make_service, make_structure, make_user


@pytest.fixture
def user():
    return make_user()


@override_settings(BACKEND_URL="https://api.example.com")
def test_structure_admin_url_points_to_the_django_admin(user):
    structure = make_structure(user)

    assert (
        structure.get_admin_url()
        == f"https://api.example.com/admin/structures/structure/{structure.id}/change/"
    )


@override_settings(BACKEND_URL="https://api.example.com")
def test_service_admin_url_points_to_the_django_admin(user):
    service = make_service()

    assert (
        service.get_admin_url()
        == f"https://api.example.com/admin/services/service/{service.id}/change/"
    )


@override_settings(BACKEND_URL="http://example:1234")
def test_admin_url_supports_a_non_https_host_with_a_port(user):
    # en développement l'API est servie en HTTP, sur le port du `runserver`
    structure = make_structure(user)

    assert structure.get_admin_url().startswith("http://example:1234/admin/")
