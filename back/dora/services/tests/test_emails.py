from datetime import timedelta
from urllib.parse import quote

import pytest
from django.conf import settings
from django.core import mail
from django.utils import timezone

from dora.core.test_utils import make_service
from dora.services.emails import send_service_notification
from dora.services.enums import ServiceStatus
from dora.services.models import Service


@pytest.fixture
def draft_service():
    service = make_service(status=ServiceStatus.DRAFT)
    user = service.structure.members.first()
    service.contact_email = user.email
    service.creation_date = timezone.now() - timedelta(
        days=settings.NUM_DAYS_BEFORE_DRAFT_SERVICE_NOTIFICATION + 1
    )

    service.save()

    return service


@pytest.fixture
def outdated_service():
    # Fréquence de mise à jour : 6 mois par défaut
    modification_date = timezone.now() - timedelta(days=200)
    service = make_service(
        status=ServiceStatus.PUBLISHED,
        modification_date=modification_date,
    )
    user = service.structure.members.first()
    service.contact_email = user.email

    service.save()

    return service


@pytest.mark.parametrize("service", ["draft_service", "outdated_service"])
def test_send_service_notification(service, request):
    service = request.getfixturevalue(service)
    user = service.structure.members.first()

    assert service in (
        Service.objects.update_advised() | Service.objects.expired_drafts()
    ), "Le service sélectionné ne fait pas l'objet d'une notification"

    # Send the notification email
    send_service_notification(user)

    # Assert that the email was sent with the correct subject and body
    assert len(mail.outbox) == 1

    email = mail.outbox[0]

    assert (
        email.subject
        == "Des mises à jour de votre offre de service sur DORA sont nécessaires"
    )
    assert user.first_name in email.body, (
        "Le nom de l'éditeur du service doit être cité dans l'e-mail"
    )

    assert quote(service.name) in email.body, (
        "Le nom du service doit apparaitre dans l'e-mail"
    )
