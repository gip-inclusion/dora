import pytest

from dora.core.test_utils import make_structure, make_structure_member, make_user
from dora.notifications.enums import NotificationStatus
from dora.notifications.models import Notification
from dora.structures.models import Structure

from ..core import Task, TaskError
from .conftest import FakeTask, StructureTask


def test_init_with_bad_model():
    with pytest.raises(
        TaskError,
        match="Le champ 'owner_notification_id' n'existe pas dans le modèle de notification",
    ):
        FakeTask()


def test_check_notification(structure_task):
    with pytest.raises(TaskError, match="Notification invalide"):
        structure_task._check(None)

    with pytest.raises(TaskError, match="Type de notification incompatible"):
        structure_task._check(Notification())

    with pytest.raises(TaskError, match="Type de notification incompatible"):
        structure_task._check(Notification(task_type="foo"))

    with pytest.raises(
        TaskError, match="Cette notification n'est pas en attente de traitement"
    ):
        structure_task._check(
            Notification(task_type="generic_task", status=NotificationStatus.COMPLETE)
        )

    n = Notification(task_type="generic_task")

    assert structure_task._check(n) == n, (
        "doit retourner la notification, si elle est valide"
    )


def test_new_notification(structure_task):
    with pytest.raises(TaskError, match="Pas de propriétaire défini"):
        structure_task._new_notification(None)

    with pytest.raises(
        TaskError, match="Le modèle de notification n'a pas de champ nommé 'owner_str'"
    ):
        structure_task._new_notification("test")

    assert isinstance(structure_task._new_notification(Structure()), Notification)


def test_registering(structure_task):
    with pytest.raises(TaskError, match="Impossible d'enregistrer cette classe"):
        Task.register(str)

    with pytest.raises(TaskError, match="Impossible de retirer cette classe"):
        Task.unregister(str)

    assert StructureTask not in Task.registered_tasks()

    Task.register(StructureTask)

    assert StructureTask in Task.registered_tasks()

    Task.unregister(StructureTask)

    assert StructureTask not in Task.registered_tasks()


def test_run_params_validity(structure_task):
    # limit :
    with pytest.raises(TaskError, match="'limit' doit être entier"):
        structure_task.run(limit="test")

    # ok :
    structure_task.run()
    structure_task.run(limit=10)


@pytest.mark.parametrize("strict,expected", [(True, 0), (False, 1)])
def test_strict_param(structure_task, strict, expected):
    good1 = structure_task._new_notification(owner=make_structure())
    good1.save()

    # génération d'une notification de structure défectueuse, voir si l'execution s'arrête
    bad = structure_task._new_notification(owner=make_structure())
    bad.counter = 42
    bad.save()

    good2 = structure_task._new_notification(owner=make_structure())
    good2.save()

    assert bad.counter == 42
    assert good1.counter == 0
    assert good2.counter == 0

    ok = errors = obsolete = 0

    if strict:
        with pytest.raises(TaskError, match="Erreur d'exécution de l'action"):
            # l'execution doit être interompue avant le traitement de good2
            ok, errors, obsolete = structure_task.run(strict=strict)
    else:
        ok, errors, obsolete = structure_task.run(strict=strict)

    good1.refresh_from_db()
    good2.refresh_from_db()

    assert good1.counter == 1
    assert good2.counter == expected
    assert (ok, errors, obsolete) == (0 if strict else 2, expected, 0)


@pytest.mark.parametrize("dry_run,expected", [(False, 1), (True, 0)])
def test_dry_run_param(structure_task, dry_run, expected):
    n = structure_task._new_notification(owner=make_structure())
    n.save()

    ok, errors, _ = structure_task.run(dry_run=dry_run)
    n.refresh_from_db()

    assert n.counter == expected
    assert (ok, errors) == (1, 0)


@pytest.mark.parametrize(
    "limit,created,expected", [(1, 0, 0), (1, 2, 1), (2, 2, 2), (2, 3, 2)]
)
def test_limit_param(structure_task, limit, created, expected):
    notifications = [
        structure_task._new_notification(owner=make_structure()) for _ in range(created)
    ]

    for n in notifications:
        n.save()

    ok, _, _ = structure_task.run(limit=limit)

    for idx, n in enumerate(notifications):
        n.refresh_from_db()
        if idx < limit:
            assert n.counter == 1
        else:
            assert n.counter == 0

    assert ok == expected


def test_complete_obsolete_notifications(structure_task):
    normal = structure_task._new_notification(owner=make_structure())
    normal.save()
    print("normal", normal.__dict__)

    assert len(structure_task.candidates()) == 1

    structure = make_structure()
    obsolete = structure_task._new_notification(owner=structure)
    obsolete.save()
    print("obsolete", obsolete.__dict__)

    assert len(structure_task.candidates()) == 2

    # on rend la notification obsolète en ajoutant un membre après la création de la notification
    make_structure_member(user=make_user(), structure=structure)

    ok, _, obs = structure_task.run()
    obsolete.refresh_from_db()
    print(obsolete.__dict__)

    assert len(structure_task.candidates()) == 1
    assert Notification.objects.count() == 2
    assert NotificationStatus.COMPLETE == obsolete.status
    assert (ok, obs) == (1, 1)


def test_create_run_querysets(structure_task):
    # Readnility counts : aurait pu être paramétrée, mais plus lisible comme ça
    new, obs = structure_task._create_run_querysets()

    assert len(structure_task.candidates()) == 0
    assert len(new) == 0
    assert len(obs) == 0

    # aucun nouveau candidats (voir définition de la tâche)
    structure_task._new_notification(owner=make_structure(user=make_user())).save()
    new, obs = structure_task._create_run_querysets()

    assert len(structure_task.candidates()) == 0
    assert len(new) == 0
    assert len(obs) == 1

    # une notification a créer, pas de notification obsolète
    make_structure()
    new, obs = structure_task._create_run_querysets()

    assert len(structure_task.candidates()) == 1
    assert len(new) == 1
    assert len(obs) == 1

    # une notification obsolète, une nouvelle notification
    make_structure()
    structure_task._new_notification(owner=make_structure(user=make_user())).save()
    new, obs = structure_task._create_run_querysets()

    assert len(structure_task.candidates()) == len(new)
    assert len(new) == 2
    assert len(obs) == 2


@pytest.mark.parametrize(
    "counter,expected",
    [(0, True), (100, True), (101, False)],
)
def test_should_trigger(structure_task, counter, expected):
    # basique : on teste juste que le déclenchement se fait bien
    # les tâches de notification "concrètes" sont créée testés
    # dans chaque module (voir par ex. `tasks.structure`)
    n = structure_task._new_notification(owner=make_structure(), counter=counter)

    assert structure_task.should_trigger(n) == expected


def test_post_process(structure_task):
    # le processus de validation des notifications doit appeler `post_process`
    # après avoir appelé `trigger`

    # ne doit rien faire
    n = structure_task._new_notification(owner=make_structure(), counter=1)
    structure_task.post_process(n)

    # doit lever une exception pour cette valeur de compteur
    # (voir conftest)
    n = structure_task._new_notification(owner=make_structure(), counter=43)
    with pytest.raises(Exception, match="post-process failed"):
        structure_task.post_process(n)
