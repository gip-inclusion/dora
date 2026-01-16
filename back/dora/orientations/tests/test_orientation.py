import pytest

from dora.core.models import LogItem
from dora.core.test_utils import make_orientation, make_published_service, make_user
from dora.orientations.models import OrientationStatus


def test_dora_service_orientation_get_service_address_line():
    service = make_published_service(
        address1="6 Boulevard St Denis",
        address2="Plateforme de l'inclusion",
        postal_code="75010",
        # on ne peut pas spécifier de ville dans le contexte d'un test
    )
    orientation = make_orientation(service=service)
    assert (
        orientation.get_service_address_line()
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010"
    )


def test_di_service_orientation_get_service_address_line():
    orientation = make_orientation(
        service=None,
        di_service_id="di_service_id",
        di_service_address_line="6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris",
    )
    assert (
        orientation.get_service_address_line()
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris"
    )


@pytest.mark.parametrize(
    "old_status,new_status",
    [
        (OrientationStatus.PENDING, OrientationStatus.ACCEPTED),
        (OrientationStatus.PENDING, OrientationStatus.REJECTED),
        (OrientationStatus.PENDING, OrientationStatus.EXPIRED),
        (OrientationStatus.MODERATION_PENDING, OrientationStatus.PENDING),
        (OrientationStatus.MODERATION_PENDING, OrientationStatus.MODERATION_REJECTED),
    ],
)
def test_set_status_creates_log_item(old_status, new_status):
    orientation = make_orientation(status=old_status)
    user = make_user()

    orientation.set_status(new_status, user=user)

    log_item = LogItem.objects.filter(orientation=orientation).latest("date")
    assert log_item.orientation == orientation
    assert log_item.user == user
    assert (
        log_item.message
        == f"Orientation passée de {old_status.label} à {new_status.label}"
    )


def test_set_status_creates_log_item_without_user():
    orientation = make_orientation(status=OrientationStatus.PENDING)

    orientation.set_status(OrientationStatus.REJECTED, user=None)

    log_item = LogItem.objects.filter(orientation=orientation).latest("date")
    assert log_item.orientation == orientation
    assert log_item.user is None
    assert (
        log_item.message
        == "Orientation passée de Ouverte / En cours de traitement à Refusée"
    )
