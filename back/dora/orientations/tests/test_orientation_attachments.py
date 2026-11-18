import os
from unittest.mock import patch

import pytest
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage

from dora.core.test_utils import make_orientation, make_published_service
from dora.orientations.models import OrientationStatus

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


@pytest.fixture
def mock_storage():
    """Mock S3/storage so attachment tests don't need real credentials."""
    stored = {}

    def save(name, content):
        stored[name] = content.read() if hasattr(content, "read") else content

    def exists(name):
        return name in stored

    def delete(name):
        stored.pop(name, None)

    with patch("dora.orientations.models.default_storage") as m:
        with patch(
            "dora.orientations.tests.test_orientation_attachments.default_storage", m
        ):
            m.save.side_effect = save
            m.exists.side_effect = exists
            m.delete.side_effect = delete
            yield m


@only_local
def test_delete_attachment_existing(orientation, mock_storage):
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
def test_delete_attachment_non_existing(orientation, mock_storage):
    # Essayer de supprimer une pièce jointe qui n'existe pas
    non_existing_path = "non_existing_attachment.txt"
    deleted_path, success = orientation.delete_attachment(non_existing_path)

    # Vérifier que la suppression a échoué
    assert deleted_path == non_existing_path
    assert not success


def test_delete_attachments_removes_orphan_references(orientation, mock_storage):
    default_storage.save("present.txt", ContentFile("Test content"))
    orientation.beneficiary_attachments = ["present.txt", "missing.txt"]
    orientation.save()

    results = orientation.delete_attachments()

    assert results == {"present.txt": True, "missing.txt": False}
    orientation.refresh_from_db()
    assert orientation.beneficiary_attachments == []


@only_local
def test_delete_attachments(orientation, mock_storage):
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
