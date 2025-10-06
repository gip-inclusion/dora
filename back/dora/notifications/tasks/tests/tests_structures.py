from datetime import timedelta

import pytest
from dateutil.relativedelta import relativedelta
from django.core import mail
from django.utils import timezone
from freezegun import freeze_time

from dora.core.constants import SIREN_FRANCE_TRAVAIL
from dora.core.test_utils import make_service, make_structure, make_user
from dora.notifications.enums import NotificationStatus, TaskType
from dora.notifications.models import Notification

from ..core import Task
from ..structures import OrphanStructuresTask, StructureServiceActivationTask

# note : le test des méthodes `candidates` peut aussi être fait au niveau
# du modèle propriétaire si la méthode consiste en un simple queryset.
# Dans le cas contraire, on peut éventuellement ajouter des tests ici.
# pas utile pour les structures orphelines en tout cas.


@pytest.fixture
def orphan_structure_task():
    return OrphanStructuresTask()


def test_orphan_structures_registered():
    assert OrphanStructuresTask in Task.registered_tasks()


def test_orphan_structure_test_should_trigger(orphan_structure_task):
    # créée telle quelle, une structure est orpheline
    make_structure(email="test@test.com")

    ok, _, _ = orphan_structure_task.run()
    n = Notification.objects.pending().first()

    # premier déclenchement immédiatement
    assert ok
    assert n.task_type == TaskType.ORPHAN_STRUCTURES
    assert n.counter == 1

    ok, _, _ = orphan_structure_task.run()
    n = Notification.objects.pending().first()

    # plus rien à traiter maitenant
    assert not ok

    for in_weeks in (2, 4, 6):
        # déclenchements toutes les 2 semaines
        with freeze_time(timezone.now() + timedelta(weeks=in_weeks)):
            ok, _, _ = orphan_structure_task.run()
            expected_count = 1 + in_weeks / 2
            n.refresh_from_db()

            # la notification a bien été déclenchée
            assert ok
            assert n.counter == expected_count

            ok, _, _ = orphan_structure_task.run()
            n.refresh_from_db()

            # à la même date :
            # une nouvelle exécution ne déclenche pas de nouvelle notification
            assert not ok
            assert n.counter == expected_count

    # à ce point la seule notification doit être clôturée
    assert len(Notification.objects.pending()) == 0
    assert n.status == NotificationStatus.COMPLETE

    ok, _, _ = orphan_structure_task.run()

    assert not ok


def test_process_orphan_structures(orphan_structure_task):
    structure = make_structure(email="jessie@pixar.com")

    ok, _, _ = orphan_structure_task.run()

    assert ok == 1
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [structure.email]

    # des tests plus complets concernant la structure et le contenu de l'email
    # sont effectués dans le module `dora.structures.tests.test_emails`


@pytest.fixture
def structure_service_activation_task():
    return StructureServiceActivationTask()


@pytest.fixture
def structure_with_admin():
    structure = make_structure()
    with freeze_time(timezone.now() - timedelta(days=42)):
        make_user(structure=structure, is_admin=True)

    return structure


def test_structure_service_activation_task_registered():
    assert StructureServiceActivationTask in Task.registered_tasks()


def test_structure_services_activation_candidates(
    structure_with_admin, structure_service_activation_task
):
    assert structure_service_activation_task.candidates()

    # la structure est une agence France Travail
    structure_with_admin.siret = SIREN_FRANCE_TRAVAIL + "12345"
    structure_with_admin.save()

    assert not structure_service_activation_task.candidates()

    # pas de structure obsolète
    structure_with_admin.siret = "50060080000001"
    structure_with_admin.is_obsolete = True
    structure_with_admin.save()

    assert not structure_service_activation_task.candidates()

    # structure avec au moins un service
    structure_with_admin.siret = "50060080000002"
    make_service(structure=structure_with_admin)
    structure_with_admin.is_obsolete = False
    structure_with_admin.save()

    assert not structure_service_activation_task.candidates()

    # admin dans la structure, mais depuis moins d'un mois
    structure_with_admin.services.first().delete()
    m = structure_with_admin.membership.first()
    m.creation_date = timezone.now()
    m.save()

    assert not structure_service_activation_task.candidates()


def test_structure_service_activation_task_should_trigger(
    structure_with_admin, structure_service_activation_task
):
    ok, _, _ = structure_service_activation_task.run()
    n = Notification.objects.pending().first()

    # premier déclenchement immédiat
    assert ok
    assert n.task_type == TaskType.SERVICE_ACTIVATION
    assert n.counter == 1

    ok, _, _ = structure_service_activation_task.run()
    n = Notification.objects.pending().first()

    # plus rien à traiter maitenant (un mois d'attente)
    assert not ok

    for in_months in (1, 2, 3, 4):
        # déclenchements toutes les mois pendant 4 mois
        with freeze_time(timezone.now() + relativedelta(months=in_months)):
            ok, _, _ = structure_service_activation_task.run()
            expected_count = 1 + in_months
            n.refresh_from_db()

            # la notification a bien été déclenchée
            assert ok, f"failed for month: {in_months}, {expected_count}, {n.counter}"
            assert n.counter == expected_count

            ok, _, _ = structure_service_activation_task.run()
            n.refresh_from_db()

            # à la même date :
            # une nouvelle exécution ne déclenche pas de nouvelle notification
            assert not ok
            assert n.counter == expected_count

    # à ce point la seule notification doit être clôturée
    assert len(Notification.objects.pending()) == 0
    assert n.status == NotificationStatus.COMPLETE

    ok, _, _ = structure_service_activation_task.run()

    assert not ok


def test_process_structure_service_activation_task(
    structure_service_activation_task, structure_with_admin
):
    ok, _, _ = structure_service_activation_task.run()

    assert ok == 1
    assert len(mail.outbox) == 1
    assert mail.outbox[0].to == [structure_with_admin.admins[0].email]
