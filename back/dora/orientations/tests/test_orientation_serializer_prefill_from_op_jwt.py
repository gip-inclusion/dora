from unittest.mock import patch

import pytest
from rest_framework import serializers

from dora.core.test_utils import make_published_service
from dora.orientations.models import Orientation
from dora.orientations.serializers import OrientationSerializer


def test_validate_prefills_beneficiary_data_from_op_jwt(monkeypatch):
    """Teste le préremplissage des données bénéficiaire depuis le JWT des Emplois."""
    service = make_published_service()

    claims = {
        "beneficiary": {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "phone": "0102030405",
            "france_travail_id": "1234567890",
            "uid": "beneficiary-uid",
        },
        "prescriber": {
            "organization": {
                "uid": "structure-uid",
            }
        },
    }

    monkeypatch.setattr(
        "dora.orientations.serializers.decode_token",
        lambda value: claims,
    )

    serializer = OrientationSerializer()
    data = {
        "service": service,
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
        "op_jwt": "fake-token",
    }

    result = serializer.validate(data)

    assert result["beneficiary_first_name"] == "John"
    assert result["beneficiary_last_name"] == "Doe"
    assert result["beneficiary_email"] == "john.doe@example.com"
    assert result["beneficiary_phone"] == "0102030405"
    assert result["beneficiary_france_travail_number"] == "1234567890"
    assert result["les_emplois_beneficiary_uid"] == "beneficiary-uid"
    assert result["les_emplois_structure_uid"] == "structure-uid"


def test_validate_with_invalid_op_jwt_raises_error(monkeypatch):
    """Teste qu'un JWT invalide lève une erreur de validation."""
    service = make_published_service()

    def _decode_token(_value):
        raise ValueError("invalid token")

    monkeypatch.setattr(
        "dora.orientations.serializers.decode_token",
        _decode_token,
    )

    serializer = OrientationSerializer()
    data = {
        "service": service,
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
        "op_jwt": "invalid-token",
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.validate(data)

    assert "op_jwt" in exc_info.value.detail
    assert str(exc_info.value.detail["op_jwt"]) == "Token JWT invalide ou expiré."


@patch("dora.orientations.serializers.decode_token")
def test_validate_does_not_use_op_jwt_for_existing_instance(mock_decode_token):
    """Teste que le JWT n'est pas utilisé pour une instance existante."""
    service = make_published_service()
    orientation = Orientation.objects.create(
        service=service,
        beneficiary_last_name="Doe",
        beneficiary_first_name="John",
        referent_last_name="Smith",
        referent_first_name="Jane",
        referent_email="jane.smith@example.com",
    )

    serializer = OrientationSerializer(instance=orientation)
    data = {
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
        "op_jwt": "should-not-be-used",
    }

    result = serializer.validate(data)

    mock_decode_token.assert_not_called()
    # Les données ne doivent pas être modifiées par le JWT
    assert result == data
