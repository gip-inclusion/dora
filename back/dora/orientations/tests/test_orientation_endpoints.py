from django.core import mail

from ..models import OrientationStatus


def test_query_refresh(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/refresh/"
    response = api_client.patch(url, follow=True)

    assert response.status_code == 204


def test_query_access(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/"
    response = api_client.get(url, follow=True)

    # permissions : pas de hash, pas d'orientation (pseudo-auth)
    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    response = api_client.get(url, follow=True)

    assert response.status_code == 200


def test_query_validate(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/validate/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "beneficiary_message": "test_beneficiary_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204
    assert orientation.status == OrientationStatus.ACCEPTED

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 4
    assert mail.outbox[0].to == [orientation.get_contact_email()]
    assert mail.outbox[1].to == [orientation.prescriber.email]
    assert mail.outbox[2].to == [orientation.referent_email]
    assert mail.outbox[3].to == [orientation.beneficiary_email]


def test_query_reject(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/reject/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
        "reasons": [],
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204
    assert orientation.status == OrientationStatus.REJECTED

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 3
    assert mail.outbox[0].to == [orientation.get_contact_email()]
    assert mail.outbox[1].to == [orientation.prescriber.email]
    assert mail.outbox[2].to == [orientation.referent_email]


def test_contact_beneficiary(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/contact/beneficiary/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [orientation.beneficiary_email]


def test_contact_prescriber(api_client, orientation):
    url = f"/orientations/{orientation.query_id}/contact/prescriber/"
    response = api_client.post(url, follow=True)

    assert response.status_code == 401

    url += f"?h={orientation.get_query_id_hash()}"
    data = {
        "message": "test_message",
    }
    response = api_client.post(url, data=data, follow=True)
    orientation.refresh_from_db()

    assert response.status_code == 204

    # on vérifie qu'un e-mail a bien été envoyé au bon destinataire
    # (vérifier le contenu n'est pas pertinent dans cette série de tests)
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [orientation.prescriber.email]
