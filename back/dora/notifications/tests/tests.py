import pytest
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError
from django.utils import timezone

from dora.core.test_utils import make_structure, make_user

from ..enums import NotificationStatus, TaskType
from ..models import Notification, NotificationError

# note : le premier type de propriétaire implémenté est la structure
# les tests du modèle se basent sur des notification ayant ce type de propriétaire


@pytest.fixture()
def notification():
    return Notification(
        owner_structure=make_structure(), task_type=TaskType.ORPHAN_STRUCTURES
    )


@pytest.mark.parametrize("status", NotificationStatus.values)
def test_notification_queryset_status(notification, status):
    notification.status = status
    notification.save()

    # ces méthodes du queryset reprennent le nom du status
    qs_method = getattr(Notification.objects, status)

    assert len(qs_method()) == 1


@pytest.mark.parametrize("status", NotificationStatus.values)
def test_notification_str(notification, status):
    notification.status = status
    assert str(notification.pk) in str(notification)
    assert notification.status in str(notification)
    assert notification.task_type in str(notification)


def test_related_objects():
    structure = make_structure()

    assert not structure.notifications.count()

    notification = Notification(
        owner_structure=structure, task_type=TaskType.GENERIC_TASK
    )
    notification.save()

    assert notification == structure.notifications.first()

    user = make_user()

    assert not user.notifications.count()

    notification = Notification(owner_user=user, task_type=TaskType.GENERIC_TASK)
    notification.save()

    assert notification == user.notifications.first()

    putative_membership = make_structure(
        putative_member=make_user()
    ).putative_membership.first()

    assert not putative_membership.notifications.count()

    notification = Notification(
        owner_structureputativemember=putative_membership,
        task_type=TaskType.GENERIC_TASK,
    )
    notification.save()

    assert notification == putative_membership.notifications.first()


def test_constraints(notification):
    notification.owner_structure = None

    with pytest.raises(IntegrityError, match="check_owner"):
        notification.save()
    ...


def test_unicity(notification):
    notification.save()

    # même type de tâche pour une structure donnée
    n = Notification(
        task_type=notification.task_type, owner_structure=notification.owner_structure
    )
    with pytest.raises(IntegrityError, match="duplicate key value"):
        n.save()
    ...


def test_owner(notification):
    assert notification.owner == notification.owner_structure

    with pytest.raises(
        NotificationError, match="Aucun propriétaire défini pour la notification"
    ):
        notification.owner_structure = None
        notification.owner

    with pytest.raises(
        NotificationError, match="Plusieurs propriétaires définis pour la notification"
    ):
        notification.owner_user = make_user()
        notification.owner_structure = make_structure()
        notification.owner


def test_expired(notification):
    assert not notification.expired

    notification.expires_at = timezone.now()

    assert notification.expired


def test_trigger(notification):
    notification.trigger()
    notification.refresh_from_db()

    assert notification.counter == 1
    assert notification.updated_at < timezone.now()


def test_complete(notification):
    notification.complete()
    notification.refresh_from_db()

    assert notification.counter == 0
    assert notification.updated_at < timezone.now()

    notification.counter = 1
    notification.complete()
    notification.refresh_from_db()

    # ne doit pas changer
    assert notification.counter == 0

    notification.expired_at = timezone.now()
    notification.status = NotificationStatus.EXPIRED
    notification.save()

    notification.complete()
    notification.refresh_from_db()

    # ne doit pas changer
    assert notification.counter == 0
    assert notification.status == NotificationStatus.EXPIRED


def test_clean(notification):
    # doit passer sans Exception
    notification.clean()

    # type inconnu
    notification.task_type = "unknown"
    with pytest.raises(ValidationError, match="Type de notification inconnu"):
        notification.clean()

    # pas de structure propriétaire
    notification.task_type = TaskType.ORPHAN_STRUCTURES
    notification.owner_structure = None
    with pytest.raises(ValidationError, match="Aucun objet propriétaire attaché"):
        notification.clean()

    # mauvais type de structure rattaché
    notification.owner_user = make_user()
    with pytest.raises(ValidationError, match="Aucune structure attachée"):
        notification.clean()

    ...
