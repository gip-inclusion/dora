import os
from unittest.mock import patch

import pytest
import requests
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from rest_framework import serializers

from dora.core.test_utils import make_orientation, make_published_service
from dora.orientations.models import Orientation, OrientationStatus
from dora.orientations.serializers import OrientationSerializer
from dora.services.models import Credential

only_local = pytest.mark.skipif(
    os.getenv("ENVIRONMENT") != "local",
    reason="Test uniquement exécuté dans l'environnement de développement",
)


@pytest.fixture
def orientation():
    service = make_published_service(
        address1="6 Boulevard St Denis",
        address2="Plateforme de l'inclusion",
        postal_code="75010",
    )
    return make_orientation(
        service=service,
        beneficiary_last_name="Doe",
        beneficiary_first_name="John",
        referent_last_name="Smith",
        referent_first_name="Jane",
        referent_email="jane.smith@example.com",
    )


@only_local
def test_delete_attachment_existing(orientation):
    # Créer une pièce jointe factice
    attachment_path = "test_attachment.txt"
    default_storage.save(attachment_path, ContentFile("Test content"))

    # Ajouter la pièce jointe à l'orientation
    orientation.beneficiary_attachments.append(attachment_path)
    orientation.save()

    # Vérifier que la pièce jointe existe avant la suppression
    assert default_storage.exists(attachment_path)

    # Supprimer la pièce jointe
    deleted_path, success = orientation.delete_attachment(attachment_path)

    # Vérifier que la pièce jointe a été supprimée
    assert not default_storage.exists(attachment_path)
    assert deleted_path == attachment_path
    assert success


@only_local
def test_delete_attachment_non_existing(orientation):
    # Essayer de supprimer une pièce jointe qui n'existe pas
    non_existing_path = "non_existing_attachment.txt"
    deleted_path, success = orientation.delete_attachment(non_existing_path)

    # Vérifier que la suppression a échoué
    assert deleted_path == non_existing_path
    assert not success


@only_local
def test_delete_attachments(orientation):
    # Créer plusieurs pièces jointes factices
    attachment_paths = ["test_attachment1.txt", "test_attachment2.txt"]
    for path in attachment_paths:
        default_storage.save(path, ContentFile("Test content"))

    # Ajouter les pièces jointes à l'orientation
    orientation.beneficiary_attachments.extend(attachment_paths)
    orientation.save()

    # Vérifier que les pièces jointes existent avant la suppression
    for path in attachment_paths:
        assert default_storage.exists(path)

    # Supprimer toutes les pièces jointes
    results = orientation.delete_attachments()

    # Vérifier que toutes les pièces jointes ont été supprimées
    for path in attachment_paths:
        assert not default_storage.exists(path)
        assert results[path]


@only_local
@patch("dora.orientations.models.default_storage.exists", return_value=True)
@patch("dora.orientations.models.default_storage.delete")
def test_delete_attachments_with_mock(mock_delete, mock_exists, orientation):
    # Ajouter des pièces jointes factices à l'orientation
    attachment_paths = ["test_attachment1.txt", "test_attachment2.txt"]
    orientation.beneficiary_attachments.extend(attachment_paths)
    orientation.save()

    # Supprimer toutes les pièces jointes
    results = orientation.delete_attachments()

    # Vérifier que les méthodes de stockage ont été appelées correctement
    for path in attachment_paths:
        mock_delete.assert_any_call(path)
        assert results[path]


# Tests pour la méthode validate
def test_validate_dora_service_with_credentials_requires_attachments():
    """Teste qu'un service Dora avec des justificatifs nécessite des pièces jointes."""
    service = make_published_service()
    # Créer un justificatif réel et l'ajouter au service
    credential = Credential.objects.create(name="Justificatif de test")
    service.credentials.add(credential)

    serializer = OrientationSerializer()
    data = {
        "service": service,
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.validate(data)

    assert "beneficiary_attachments" in exc_info.value.detail
    assert "vous devez ajouter les documents demandés" in str(
        exc_info.value.detail["beneficiary_attachments"]
    )


def test_validate_dora_service_with_forms_requires_attachments():
    """Teste qu'un service Dora avec des formulaires nécessite des pièces jointes."""
    service = make_published_service()
    # Mock du service pour avoir des formulaires
    with patch.object(service, "forms", ["form1", "form2"]):
        serializer = OrientationSerializer()
        data = {
            "service": service,
            "beneficiary_attachments": [],
            "data_protection_commitment": True,
        }

        with pytest.raises(serializers.ValidationError) as exc_info:
            serializer.validate(data)

        assert "beneficiary_attachments" in exc_info.value.detail


def test_validate_dora_service_with_attachments_passes():
    """Teste qu'un service Dora avec des justificatifs requis mais avec des pièces jointes passe la validation."""
    service = make_published_service()
    # Créer un justificatif réel et l'ajouter au service
    credential = Credential.objects.create(name="Justificatif de test")
    service.credentials.add(credential)

    serializer = OrientationSerializer()
    data = {
        "service": service,
        "beneficiary_attachments": ["document.pdf"],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


def test_validate_dora_service_no_requirements_passes():
    """Teste qu'un service Dora sans justificatifs ni formulaires passe la validation."""
    service = make_published_service()
    # Le service n'a pas de justificatifs ni de formulaires par défaut
    serializer = OrientationSerializer()
    data = {
        "service": service,
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


@patch("dora.orientations.serializers.dora.data_inclusion.di_client_factory")
@patch("dora.orientations.serializers.dora.data_inclusion.map_service")
def test_validate_di_service_with_credentials_requires_attachments(
    mock_map_service, mock_client_factory
):
    """Teste qu'un service DI avec des justificatifs nécessite des pièces jointes."""
    # Mock du client DI et du service
    mock_client = mock_client_factory.return_value
    # Données d'un service DI
    mock_client.retrieve_service.return_value = {
        "id": "test-service-id",
        "nom": "Service Test",
        "justificatifs": ["doc1", "doc2"],
        "source": "soliguide",
    }
    mock_map_service.return_value = {"credentials": ["doc1", "doc2"]}

    serializer = OrientationSerializer()
    data = {
        "di_service_id": "soliguide--test-service-id",
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.validate(data)

    assert "beneficiary_attachments" in exc_info.value.detail


@patch("dora.orientations.serializers.dora.data_inclusion.di_client_factory")
@patch("dora.orientations.serializers.dora.data_inclusion.map_service")
def test_validate_di_service_with_attachments_passes(
    mock_map_service, mock_client_factory
):
    """Teste qu'un service DI avec des justificatifs requis mais avec des pièces jointes passe la validation."""
    # Mock du client DI et du service
    mock_client = mock_client_factory.return_value
    # Données d'un service DI
    mock_client.retrieve_service.return_value = {
        "id": "test-service-id",
        "nom": "Service Test",
        "justificatifs": ["doc1", "doc2"],
        "source": "soliguide",
    }
    mock_map_service.return_value = {"credentials": ["doc1", "doc2"]}

    serializer = OrientationSerializer()
    data = {
        "di_service_id": "soliguide--test-service-id",
        "beneficiary_attachments": ["document.pdf"],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


@patch("dora.orientations.serializers.dora.data_inclusion.di_client_factory")
@patch("dora.orientations.serializers.dora.data_inclusion.map_service")
def test_validate_di_service_no_requirements_passes(
    mock_map_service, mock_client_factory
):
    """Teste qu'un service DI sans justificatifs ni formulaires passe la validation."""
    # Mock du client DI et du service
    mock_client = mock_client_factory.return_value
    # Données réalistes d'un service DI sans justificatifs ni formulaires
    mock_client.retrieve_service.return_value = {
        "id": "test-service-id",
        "nom": "Service Test",
        "justificatifs": None,
        "formulaire_en_ligne": None,
        "source": "soliguide",
    }
    mock_map_service.return_value = {"credentials": None, "forms": None}

    serializer = OrientationSerializer()
    data = {
        "di_service_id": "soliguide--test-service-id",
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


@patch("dora.orientations.serializers.dora.data_inclusion.di_client_factory")
def test_validate_di_service_connection_error_passes(mock_client_factory):
    """Teste qu'un service DI avec une erreur de connexion passe la validation."""
    # Mock du client DI pour lever une ConnectionError
    mock_client = mock_client_factory.return_value
    mock_client.retrieve_service.side_effect = requests.ConnectionError()

    serializer = OrientationSerializer()
    data = {
        "di_service_id": "soliguide--test-service-id",
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


@patch("dora.orientations.serializers.dora.data_inclusion.di_client_factory")
def test_validate_di_service_none_response_passes(mock_client_factory):
    """Teste qu'un service DI avec une réponse None passe la validation."""
    # Mock du client DI pour retourner None
    mock_client = mock_client_factory.return_value
    mock_client.retrieve_service.return_value = None

    serializer = OrientationSerializer()
    data = {
        "di_service_id": "soliguide--test-service-id",
        "beneficiary_attachments": [],
        "data_protection_commitment": True,
    }

    result = serializer.validate(data)
    assert result == data


def test_validate_existing_instance_service():
    """Teste la validation avec une instance existante qui a un service."""
    service = make_published_service()
    # Créer un justificatif réel et l'ajouter au service
    credential = Credential.objects.create(name="Justificatif de test")
    service.credentials.add(credential)

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
    }

    with pytest.raises(serializers.ValidationError) as exc_info:
        serializer.validate(data)

    assert "beneficiary_attachments" in exc_info.value.detail


@patch("dora.orientations.models.default_storage.delete")
@patch("dora.orientations.models.default_storage.exists", return_value=True)
def test_reject_orientation_deletes_attachments(
    mock_exists, mock_delete, api_client, orientation
):
    """Teste que les attachments sont supprimés lorsqu'une orientation est rejetée."""
    # Création de plusieurs pièces jointes factices et ajout à l'orientation
    attachment_paths = ["test_attachment1.txt", "test_attachment2.txt"]
    orientation.beneficiary_attachments = attachment_paths
    orientation.save()

    # Vérification que les pièces jointes existent avant le rejet
    assert len(orientation.beneficiary_attachments) == 2

    # Rejet de l'orientation via l'API
    url = f"/orientations/{orientation.query_id}/reject/?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "reasons": [],
    }
    response = api_client.post(url, data=data, follow=True)

    # Vérification que la requête a réussi
    assert response.status_code == 204

    # Rechargement de l'orientation depuis la base de données
    orientation.refresh_from_db()

    # Vérification que toutes les pièces jointes ont été supprimées du stockage
    assert mock_delete.call_count == len(attachment_paths)
    for path in attachment_paths:
        mock_delete.assert_any_call(path)

    # Vérification que la liste des pièces jointes est vide dans l'orientation
    assert len(orientation.beneficiary_attachments) == 0

    assert orientation.status == OrientationStatus.REJECTED
