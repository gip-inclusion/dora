"""Contacts non publics : absents de la liste des services, réservés aux connectés sur la fiche structure."""

import pytest

from dora.core.test_utils import make_published_service, make_structure, make_user

CONTACT = {
    "contact_name": "FOO",
    "contact_phone": "0102030405",
    "contact_email": "foo@bar.buz",
}
MASKED = {"contact_name": "", "contact_phone": "", "contact_email": ""}


def _contact(data):
    return {field: data[field] for field in CONTACT}


def test_service_list_does_not_expose_contact_info(api_client):
    make_published_service(is_contact_info_public=False, **CONTACT)

    response = api_client.get("/services/")

    assert response.status_code == 200
    [service] = response.data
    assert not CONTACT.keys() & service.keys()


@pytest.mark.parametrize(
    "is_authenticated,is_public,expected",
    [
        (False, False, MASKED),
        (False, True, CONTACT),
        (True, False, CONTACT),
    ],
)
def test_structure_services_contact_info(
    api_client, is_authenticated, is_public, expected
):
    structure = make_structure()
    make_published_service(
        structure=structure, is_contact_info_public=is_public, **CONTACT
    )
    if is_authenticated:
        # utilisateur sans structure ni e-mail validé : être connecté suffit
        api_client.force_authenticate(user=make_user(is_valid=False))

    response = api_client.get(f"/structures/{structure.slug}/")

    assert response.status_code == 200
    [service] = response.data["services"]
    assert _contact(service) == expected
