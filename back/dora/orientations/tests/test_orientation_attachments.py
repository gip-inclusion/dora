from unittest.mock import patch

import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from dora.core.test_utils import make_published_service
from dora.orientations.models import Orientation


@pytest.fixture
def orientation():
    service = make_published_service(
        address1="6 Boulevard St Denis",
        address2="Plateforme de l'inclusion",
        postal_code="75010",
    )
    return Orientation.objects.create(
        service=service,
        beneficiary_last_name="Doe",
        beneficiary_first_name="John",
        referent_last_name="Smith",
        referent_first_name="Jane",
        referent_email="jane.smith@example.com",
    )


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


def test_delete_attachment_non_existing(orientation):
    # Essayer de supprimer une pièce jointe qui n'existe pas
    non_existing_path = "non_existing_attachment.txt"
    deleted_path, success = orientation.delete_attachment(non_existing_path)

    # Vérifier que la suppression a échoué
    assert deleted_path == non_existing_path
    assert not success


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
    print("attn:", orientation.beneficiary_attachments)
    results = orientation.delete_attachments()
    print("results:", results)
    print("attn:", orientation.beneficiary_attachments)

    # Vérifier que toutes les pièces jointes ont été supprimées
    for path in attachment_paths:
        assert not default_storage.exists(path)
        assert results[path]


@patch("dora.orientations.models.default_storage.exists")
@patch("dora.orientations.models.default_storage.delete")
def test_delete_attachments_with_mock(mock_delete, mock_exists, orientation):
    # Configurer le mock pour simuler l'existence des pièces jointes
    mock_exists.return_value = True

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
