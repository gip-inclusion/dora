import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from dora.notifications.enums import TaskType
from dora.notifications.models import Notification
from dora.users.emails import (
    send_account_deletion_notification,
    send_user_without_structure_notification,
)
from dora.users.models import User

from .core import Task, TaskError

"""
Users :
    Notifications ayant pour candidats des utilisateurs "en direct",
    c.a.d. sans passer par l'intermédiaire d'un objet tiers,
    comme une invitation ou une structure.
"""

logger = logging.getLogger("dora.logs.core")


class UsersWithoutStructureTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.USERS_WITHOUT_STRUCTURE

    @classmethod
    def candidates(cls):
        return User.objects.exclude(ic_id=None).filter(
            is_valid=True,
            membership=None,
            putative_membership=None,
            date_joined__gt=timezone.now() - relativedelta(months=4, days=1),
        )

    @classmethod
    def should_trigger(cls, notification: Notification) -> bool:
        now = timezone.now()
        match notification.counter:
            case 0:
                return notification.created_at + relativedelta(days=1) <= now
            case 1:
                return notification.created_at + relativedelta(days=5) <= now
            case 2:
                return notification.created_at + relativedelta(days=10) <= now
            case 3:
                return notification.created_at + relativedelta(days=15) <= now
            case 4:
                return notification.created_at + relativedelta(months=4) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        match notification.counter:
            case 0 | 1 | 2 | 3:
                try:
                    send_user_without_structure_notification(
                        notification.owner_user, deletion=notification.counter == 3
                    )
                except Exception as ex:
                    raise TaskError(
                        f"Erreur d'envoi du mail pour un utilisateur sans structure ({notification}) : {ex}"
                    ) from ex
            case 4:
                notification.complete()
                # action : voir post_process
            case _:
                raise TaskError(f"État du compteur incohérent ({notification})")

    @classmethod
    def post_process(cls, notification: Notification):
        if notification.is_complete:
            user = notification.owner_user
            # suppression du compte utilisateur associé si :
            # - aucune autre invitation
            # - non membre d'une structure
            if not user.putative_membership.count() and not user.membership.count():
                logger.warning(
                    "Suppression d'utilisateur",
                    {
                        "legal": True,
                        "userEmail": user.email,
                        "userId": user.pk,
                        "reason": "Aucun rattachement ou invitation à une structure après relances",
                    },
                )
                user.delete()
                # à ce point, la notification doit aussi être détruite (CASCADE)...


class UserAccountDeletionTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.USER_ACCOUNT_DELETION

    @classmethod
    def candidates(cls):
        # CAT 5 :
        # les utilisateurs "actifs" qui ne se sont pas connecté depuis plus de 2 ans
        return User.objects.filter(
            is_active=True, last_login__lte=timezone.now() - relativedelta(years=2)
        )

    @classmethod
    def should_trigger(cls, notification: Notification) -> bool:
        now = timezone.now()

        match notification.counter:
            case 0:
                # on notifie immédiatement :
                return notification.created_at <= now
            case 1:
                return notification.created_at + relativedelta(days=30) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        match notification.counter:
            case 0:
                try:
                    send_account_deletion_notification(notification.owner_user)
                except Exception as ex:
                    raise TaskError(
                        f"Erreur à l'envoi de l'e-mail de suppression de compte ({notification})"
                    ) from ex
            case 1:
                # la notification se termine
                # pour l'action sur le propriétaire : voir `post_process`
                notification.complete()
            case _:
                raise TaskError(f"Incohérence de compteur ({notification})")

    @classmethod
    def post_process(cls, notification: Notification):
        if notification.is_complete:
            user = notification.owner_user

            logger.warning(
                "Suppression d'utilisateur",
                {
                    "legal": True,
                    "userEmail": user.email,
                    "userId": user.pk,
                    "reason": "Inactivité de longue durée",
                },
            )

            user.delete()
            # à ce point, la notification est détruite en cascade


Task.register(UsersWithoutStructureTask)
Task.register(UserAccountDeletionTask)
