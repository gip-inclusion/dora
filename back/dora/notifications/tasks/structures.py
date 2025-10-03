from datetime import timedelta

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.utils import timezone

from dora.core import constants
from dora.notifications.enums import TaskType
from dora.notifications.models import Notification
from dora.structures.emails import (
    send_orphan_structure_notification,
    send_structure_activation_notification,
)
from dora.structures.models import Structure

from .core import Task, TaskError


class OrphanStructuresTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.ORPHAN_STRUCTURES

    @classmethod
    def candidates(cls):
        return Structure.objects.orphans().exclude(email="")

    @classmethod
    def should_trigger(cls, notification: Notification) -> bool:
        now = timezone.now()

        # il y a plus concis, mais cette version est plus lisible :
        # une notification tout de suite, puis 3 notifications à 2 semaines d'intervalle
        match notification.counter:
            case 0:
                return notification.created_at < now
            case 1:
                return notification.created_at + timedelta(weeks=2) <= now
            case 2:
                return notification.created_at + timedelta(weeks=4) <= now
            case 3:
                return notification.created_at + timedelta(weeks=6) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        try:
            send_orphan_structure_notification(notification.owner_structure)
        except Exception as ex:
            raise TaskError(f"Erreur d'envoi du mail ({notification}) : {ex}") from ex
        else:
            if notification.counter == 3:
                # cloturée au bout de 4 envois
                notification.complete()


class StructureServiceActivationTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.SERVICE_ACTIVATION

    @classmethod
    def candidates(cls):
        # structures sans services, hors agences FT
        # avec au moins un admin inscrit depuis un mois
        one_month_ago = timezone.now() - relativedelta(months=1)
        return (
            Structure.objects.exclude(
                Q(siret__startswith=constants.SIREN_FRANCE_TRAVAIL)
                | Q(is_obsolete=True),
            )
            .filter(
                services=None,
                membership__is_admin=True,
                membership__creation_date__lt=one_month_ago,
            )
            .distinct()
        )

    @classmethod
    def should_trigger(cls, notification: Notification) -> bool:
        now = timezone.now()
        match notification.counter:
            # note : `dateutil.relativedelta` utilisé pour plus de clarté,
            # mais `timedelta` exprimé en semaines est possible aussi
            case 0:
                return notification.created_at <= now
            case 1:
                return notification.created_at + relativedelta(months=1) <= now
            case 2:
                return notification.created_at + relativedelta(months=2) <= now
            case 3:
                return notification.created_at + relativedelta(months=3) <= now
            case 4:
                return notification.created_at + relativedelta(months=4) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        try:
            send_structure_activation_notification(notification.owner_structure)
        except Exception as ex:
            raise TaskError(
                f"Erreur d'envoi du mail de relance d'activation de service ({notification}) : {ex}"
            ) from ex
        else:
            if notification.counter == 4:
                # cloturée au bout de 5 envois
                notification.complete()


# activation des tâches concernant les structures

Task.register(OrphanStructuresTask)
Task.register(StructureServiceActivationTask)
