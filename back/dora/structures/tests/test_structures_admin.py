from unittest.mock import patch

from django.contrib.messages import get_messages
from django.core import mail
from django.urls import reverse
from django.utils import timezone
from freezegun import freeze_time

from dora.core.models import ModerationStatus
from dora.core.test_utils import make_orientation, make_structure, make_user
from dora.orientations.models import OrientationStatus
from dora.structures.models import StructurePutativeMember


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


@freeze_time("2022-01-01")
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

    assert orientation_moderation_pending_1.processing_date == timezone.now()
    assert orientation_moderation_pending_2.processing_date == timezone.now()

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

    # Vérification de la redirection vers la page listant les structures en attente de modération
    assert response.status_code == 200
    structure_list_url = reverse("admin:structures_structure_changelist")
    pending_moderation_structure_list_url = (
        f"{structure_list_url}?pending_moderation=pending_moderation"
    )
    assert response.redirect_chain[-1][0] == pending_moderation_structure_list_url

    # Simulation d'une deuxième approbation à la suite

    # Appel de l'action via le client admin
    response = admin_client.post(url, follow=True)

    # Vérification du message indiquant que la structure a déjà été modérée
    messages = list(get_messages(response.wsgi_request))
    assert any(
        "n’est pas (ou plus) en attente de modération. Votre action a été ignorée."
        in message.message
        for message in messages
    )

    # Vérification de la redirection vers la page listant les structures en attente de modération
    assert response.status_code == 200
    structure_list_url = reverse("admin:structures_structure_changelist")
    pending_moderation_structure_list_url = (
        f"{structure_list_url}?pending_moderation=pending_moderation"
    )
    assert response.redirect_chain[-1][0] == pending_moderation_structure_list_url


@patch("dora.orientations.models.default_storage.exists", return_value=True)
@patch("dora.orientations.models.default_storage.delete")
def test_moderation_reject(mock_delete, mock_exists, admin_client):
    # Création de la structure
    structure = make_structure(
        moderation_status=ModerationStatus.NEED_INITIAL_MODERATION
    )

    # Création des utilisateurs membres
    members = []
    for is_admin in (True, False):
        for is_active in (True, False):
            user = make_user(
                structure=structure, is_admin=is_admin, is_active=is_active
            )
            members.append(user)

    # Création des utilisateurs membres potentiels
    putative_members = []
    for is_active in (True, False):
        for invited_by_admin in (True, False):
            for is_admin in (True, False):
                user = make_user(is_active=is_active)
                StructurePutativeMember.objects.create(
                    user=user,
                    structure=structure,
                    invited_by_admin=invited_by_admin,
                    is_admin=is_admin,
                )
                putative_members.append(user)

    # Création de deux orientations avec le statut MODERATION_PENDING
    orientation_moderation_pending_1 = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.MODERATION_PENDING,
    )
    orientation_moderation_pending_2 = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.MODERATION_PENDING,
    )

    attachment_paths_1 = ["test_attachment1.txt", "test_attachment2.txt"]
    orientation_moderation_pending_1.beneficiary_attachments = attachment_paths_1
    orientation_moderation_pending_1.save()
    attachment_paths_2 = ["test_attachment3.txt"]
    orientation_moderation_pending_2.beneficiary_attachments = attachment_paths_2
    orientation_moderation_pending_2.save()

    # Création d'autres orientations avec les autres statuts
    orientation_moderation_rejected = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.MODERATION_REJECTED,
    )
    orientation_pending = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.PENDING,
    )
    orientation_accepted = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.ACCEPTED,
    )
    orientation_rejected = make_orientation(
        prescriber_structure=structure,
        prescriber=members[0],
        status=OrientationStatus.REJECTED,
    )

    # Construction de l'URL de l'action de modération Rejeter
    url = reverse("admin:moderation_reject", args=[structure.pk])

    # Appel de l'action via le client admin
    response = admin_client.post(url, follow=True)

    # Rechargement de la structure, des utilisateurs et des orientations depuis la base de données
    structure.refresh_from_db()
    for member in members:
        member.refresh_from_db()
    for putative_member in putative_members:
        putative_member.refresh_from_db()
    orientation_moderation_pending_1.refresh_from_db()
    orientation_moderation_pending_2.refresh_from_db()
    orientation_moderation_rejected.refresh_from_db()
    orientation_pending.refresh_from_db()
    orientation_accepted.refresh_from_db()
    orientation_rejected.refresh_from_db()

    # Vérification que les e-mails ont été envoyés à tous les membres et membres potentiels de la structure
    assert len(mail.outbox) == len(members) + len(putative_members)

    # Vérification que tous les membres et membres potentiels de la structure ont été détachés
    assert structure.members.count() == 0
    assert structure.putative_members.count() == 0

    # Vérification que tous les membres et membres potentiels de la structure ont été désactivés
    assert all([not member.is_active for member in members])
    assert all([not putative_member.is_active for putative_member in putative_members])

    # Vérification que la structure est passée au statut de modération Nouvelle modération nécessaire
    assert structure.moderation_status == ModerationStatus.NEED_NEW_MODERATION

    # Vérification que les deux orientations avec le statut MODERATION_PENDING sont passées au statut MODERATION_REJECTED
    assert (
        orientation_moderation_pending_1.status == OrientationStatus.MODERATION_REJECTED
    )
    assert (
        orientation_moderation_pending_2.status == OrientationStatus.MODERATION_REJECTED
    )

    # Vérification que les pièces jointes des deux orientations avec le statut MODERATION_PENDING ont été supprimées du stockage
    all_attachment_paths = attachment_paths_1 + attachment_paths_2
    assert mock_delete.call_count == len(all_attachment_paths)
    for path in all_attachment_paths:
        mock_delete.assert_any_call(path)

    # Vérification que la liste des pièces jointes est vide dans les orientations
    assert len(orientation_moderation_pending_1.beneficiary_attachments) == 0
    assert len(orientation_moderation_pending_2.beneficiary_attachments) == 0

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
        "a été rejeté. Les demandes d’orientation en attente ont été supprimées"
        in message.message
        for message in messages
    )

    # Vérification de la redirection vers la page listant les structures en attente de modération
    assert response.status_code == 200
    structure_list_url = reverse("admin:structures_structure_changelist")
    pending_moderation_structure_list_url = (
        f"{structure_list_url}?pending_moderation=pending_moderation"
    )
    assert response.redirect_chain[-1][0] == pending_moderation_structure_list_url

    # Simulation d'un deuxième rejet à la suite

    # Appel de l'action via le client admin
    response = admin_client.post(url, follow=True)

    # Vérification du message indiquant que la structure a déjà été modérée
    messages = list(get_messages(response.wsgi_request))
    assert any(
        "n’est pas (ou plus) en attente de modération. Votre action a été ignorée."
        in message.message
        for message in messages
    )

    # Vérification de la redirection vers la page listant les structures en attente de modération
    assert response.status_code == 200
    structure_list_url = reverse("admin:structures_structure_changelist")
    pending_moderation_structure_list_url = (
        f"{structure_list_url}?pending_moderation=pending_moderation"
    )
    assert response.redirect_chain[-1][0] == pending_moderation_structure_list_url
