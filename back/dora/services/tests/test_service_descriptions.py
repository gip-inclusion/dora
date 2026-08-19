from model_bakery import baker

from dora.core.test_utils import make_published_service, make_structure


def test_service_exposes_description_and_its_alias(api_client):
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    assert api_client.get(f"/services/{service.slug}/").data["full_desc"] == "Avant"

    response = api_client.patch(f"/services/{service.slug}/", {"full_desc": "Après"})

    assert response.status_code == 200
    service.refresh_from_db()
    assert service.description == "Après"


def test_alias_takes_precedence_over_description(api_client):
    # Ce que poste un front non basculé : il édite `full_desc` et réexpédie tel quel le
    # `description` reçu au chargement. Retenir ce dernier annulerait la modification.
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    api_client.patch(
        f"/services/{service.slug}/",
        {"full_desc": "Après", "description": "Avant"},
    )

    service.refresh_from_db()
    assert service.description == "Après"
