import pytest
from django.contrib.messages import get_messages
from django.urls import reverse

from dora.core.models import ModerationStatus
from dora.core.test_utils import make_orientation, make_structure
from dora.orientations.models import OrientationStatus


@pytest.mark.django_db
def test_moderation_template(admin_client):
    # Création de la structure
    structure = make_structure(
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION
    )

    # Création d'orientations avec le statut tous les statuts possibles
    orientation_moderation_pending = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.MODERATION_PENDING
    )
    orientation_moderation_rejected = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.MODERATION_REJECTED
    )
    orientation_pending = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.PENDING
    )
    orientation_accepted = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.ACCEPTED
    )
    orientation_rejected = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.REJECTED
    )

    # Construction de l'URL de la page de modification de structure
    url = reverse("admin:structures_structure_change", args=[structure.pk])

    # Appel de la page via le client admin
    response = admin_client.get(url)

    # Vérification du succès de la requête
    assert response.status_code == 200

    # Vérification que la page contient bien la section de modération
    assert "Modération du rattachement".encode("utf-8") in response.content

    # Suppression de l'orientation ayant le statut MODERATION_PENDING
    orientation_moderation_pending.delete()

    # Appel de la page via le client admin
    response = admin_client.get(url)

    # Vérification du succès de la requête
    assert response.status_code == 200

    # Vérification que la page ne contient pas la section de modération
    assert "Modération du rattachement".encode("utf-8") not in response.content

    # Suppression de toutes les autres orientations
    orientation_moderation_rejected.delete()
    orientation_pending.delete()
    orientation_accepted.delete()
    orientation_rejected.delete()

    # Appel de la page via le client admin
    response = admin_client.get(url)

    # Vérification du succès de la requête
    assert response.status_code == 200

    # Vérification que la page ne contient pas la section de modération
    assert "Modération du rattachement".encode("utf-8") not in response.content


@pytest.mark.django_db
def test_moderation_approve(admin_client):
    # Création de la structure
    structure = make_structure(
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION
    )

    # Création de deux orientations avec le statut MODERATION_PENDING
    orientation_moderation_pending_1 = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.MODERATION_PENDING
    )
    orientation_moderation_pending_2 = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.MODERATION_PENDING
    )

    # Création d'autres orientations avec les autres statuts
    orientation_moderation_rejected = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.MODERATION_REJECTED
    )
    orientation_pending = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.PENDING
    )
    orientation_accepted = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.ACCEPTED
    )
    orientation_rejected = make_orientation(
        prescriber_structure=structure, status=OrientationStatus.REJECTED
    )

    # Construction de l'URL de l'action de modération Approuver
    url = reverse("admin:moderation_approve", args=[structure.pk])

    # Appel de l'action via le client admin
    response = admin_client.post(url, follow=True)

    # Rechargement de la structure et des orientations depuis la base de données
    structure.refresh_from_db()
    orientation_moderation_pending_1.refresh_from_db()
    orientation_moderation_pending_2.refresh_from_db()
    orientation_moderation_rejected.refresh_from_db()
    orientation_pending.refresh_from_db()
    orientation_accepted.refresh_from_db()
    orientation_rejected.refresh_from_db()

    # Vérification que la structure est passée au statut de modération Validée
    assert structure.moderation_status == ModerationStatus.VALIDATED

    # Vérification que les deux orientations avec le statut MODERATION_PENDING sont passées au statut PENDING
    assert orientation_moderation_pending_1.status == OrientationStatus.PENDING
    assert orientation_moderation_pending_2.status == OrientationStatus.PENDING

    # Vérification que les autres orientations n'ont pas vu leur statut changer
    assert (
        orientation_moderation_rejected.status == OrientationStatus.MODERATION_REJECTED
    )
    assert orientation_pending.status == OrientationStatus.PENDING
    assert orientation_accepted.status == OrientationStatus.ACCEPTED
    assert orientation_rejected.status == OrientationStatus.REJECTED

    # Vérification du message de succès
    messages = list(get_messages(response.wsgi_request))
    assert any(
        "a été approuvé. Les demandes d’orientation en attente ont été transmises"
        in message.message
        for message in messages
    )

    # Vérification de la redirection vers la page de modification de la structure
    assert response.status_code == 200
    assert response.redirect_chain[-1][0] == reverse(
        "admin:structures_structure_change", args=[structure.pk]
    )
