from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from django.conf import settings
from model_bakery import baker

from dora.core.test_utils import make_service, make_structure, make_user
from dora.sirene.models import Establishment
from dora.structures.models import StructureMember


URL = "/orientations/emplois/beneficiary-info/"

BENEFICIARY_DATA = {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone": "0102030405",
    "france_travail_id": "1234567890",
}


def test_orientation_beneficiary_info_requires_auth(api_client):
    response = api_client.get(URL)

    assert response.status_code == 401


def test_orientation_beneficiary_info_returns_beneficiary_data(api_client):
    user = make_user()
    structure = make_structure(siret="12345678901234")
    baker.make(Establishment, siret=structure.siret)
    baker.make(StructureMember, structure=structure, user=user)

    claims = {
        "prescriber": {
            "email": user.email,
            "organization": {"siret": structure.siret},
        },
        "beneficiary": BENEFICIARY_DATA,
    }

    api_client.force_authenticate(user=user)

    with (
        patch("dora.orientations.serializers.decode_token", return_value=claims),
        patch("dora.orientations.views.decode_token", return_value=claims),
    ):
        response = api_client.get(
            f"{URL}?op=fake-token&service_slug={make_service().slug}"
        )

    assert response.status_code == 200
    assert response.data == BENEFICIARY_DATA


def test_orientation_beneficiary_info_invalid_token_returns_error(
    api_client, monkeypatch
):
    user = make_user()
    api_client.force_authenticate(user=user)

    def _decode_token(_value):
        raise ValueError("invalid token")

    monkeypatch.setattr(
        "dora.orientations.serializers.decode_token",
        _decode_token,
    )

    response = api_client.get(f"{URL}?op=invalid-token")

    assert response.status_code == 400
    assert len(response.data["op"]) == 1
    assert response.data["op"][0]["message"] == "Token JWT invalide."


def test_orientation_beneficiary_info_missing_beneficiary_data_returns_error(
    api_client, monkeypatch
):
    user = make_user()
    api_client.force_authenticate(user=user)

    claims_without_beneficiary = {"foo": "bar"}

    monkeypatch.setattr(
        "dora.orientations.serializers.decode_token",
        lambda value: claims_without_beneficiary,
    )

    response = api_client.get(f"{URL}?op=valid-token-without-beneficiary")

    assert response.status_code == 400
    assert len(response.data["op"]) == 1
    assert (
        response.data["op"][0]["message"] == "Données bénéficiaire absentes du token."
    )


def test_user_with_different_email_redirects_to_homepage_with_link_invalid_param(
    api_client,
):
    user = make_user()
    api_client.force_authenticate(user=user)

    claims = {
        "prescriber": {
            "email": "different@invalid.com",
            "organization": {"siret": "12345678901234"},
        },
        "beneficiary": BENEFICIARY_DATA,
    }

    with (
        patch("dora.orientations.serializers.decode_token", return_value=claims),
        patch("dora.orientations.views.decode_token", return_value=claims),
    ):
        response = api_client.get(f"{URL}?op=fake-token")

    assert response.status_code == 200
    assert response.data["next_url"] == f"{settings.FRONTEND_URL}?link_invalid=true"


def test_no_structure_for_establishment_redirects_to_rattachement_with_orienter(
    api_client,
):
    user = make_user()
    service = make_service()
    orphan_siret = "11111111111111"
    baker.make(Establishment, siret=orphan_siret)

    claims = {
        "prescriber": {
            "email": user.email,
            "organization": {"siret": orphan_siret},
        },
        "beneficiary": BENEFICIARY_DATA,
    }

    api_client.force_authenticate(user=user)

    with (
        patch("dora.orientations.serializers.decode_token", return_value=claims),
        patch("dora.orientations.views.decode_token", return_value=claims),
    ):
        response = api_client.get(f"{URL}?op=fake-token&service_slug={service.slug}")

    assert response.status_code == 200
    parsed = urlparse(response.data["next_url"])
    query_params = parse_qs(parsed.query)
    assert parsed.path == "/auth/rattachement"
    assert query_params["siret"] == [orphan_siret]
    assert query_params["op"] == ["fake-token"]
    assert query_params["service_slug"] == [service.slug]
    assert query_params["orienter"] == ["true"]


def test_user_not_structure_member_redirects_to_rattachement_with_orienter(
    api_client,
):
    user = make_user()
    service = make_service()
    structure = make_structure(siret="12345678901234")
    baker.make(Establishment, siret=structure.siret)

    claims = {
        "prescriber": {
            "email": user.email,
            "organization": {"siret": structure.siret},
        },
        "beneficiary": BENEFICIARY_DATA,
    }

    api_client.force_authenticate(user=user)

    with (
        patch("dora.orientations.serializers.decode_token", return_value=claims),
        patch("dora.orientations.views.decode_token", return_value=claims),
    ):
        response = api_client.get(f"{URL}?op=fake-token&service_slug={service.slug}")

    assert response.status_code == 200
    parsed = urlparse(response.data["next_url"])
    query_params = parse_qs(parsed.query)
    assert parsed.path == "/auth/rattachement"
    assert query_params["siret"] == [structure.siret]
    assert query_params["service_slug"] == [service.slug]
    assert query_params["orienter"] == ["true"]
    assert query_params["fast_track"] == ["true"]
