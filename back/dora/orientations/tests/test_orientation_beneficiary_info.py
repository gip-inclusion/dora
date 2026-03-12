from dora.core.test_utils import make_user


def test_orientation_beneficiary_info_requires_auth(api_client):
    url = "/orientations/emplois/beneficiary-info/"

    response = api_client.get(url)

    assert response.status_code == 401


def test_orientation_beneficiary_info_returns_beneficiary_data(api_client, monkeypatch):
    user = make_user()
    api_client.force_authenticate(user=user)

    claims = {
        "beneficiary": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "0102030405",
            "france_travail_id": "1234567890",
        }
    }

    monkeypatch.setattr(
        "dora.orientations.serializers.decode_token",
        lambda value: claims,
    )

    url = "/orientations/emplois/beneficiary-info/?op=fake-token"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data == {
        "first_name": "John",
        "last_name": "Doe",
        "email": "john.doe@example.com",
        "phone": "0102030405",
        "france_travail_id": "1234567890",
    }


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

    url = "/orientations/emplois/beneficiary-info/?op=invalid-token"
    response = api_client.get(url)

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

    url = "/orientations/emplois/beneficiary-info/?op=valid-token-without-beneficiary"
    response = api_client.get(url)

    assert response.status_code == 400
    assert len(response.data["op"]) == 1
    assert (
        response.data["op"][0]["message"] == "Données bénéficiaire absentes du token."
    )
