import logging

from dateutil.relativedelta import relativedelta
from django.utils import timezone

from dora.notifications.enums import TaskType
from dora.notifications.models import Notification
from dora.structures.emails import (
    send_admin_invited_users_20_notification,
    send_admin_invited_users_90_notification,
    send_admin_self_invited_users_notification,
)
from dora.structures.models import StructurePutativeMember
from dora.users.emails import send_invitation_reminder

from .core import Task, TaskError

logger = logging.getLogger("dora.logs.core")


class InvitedUsersTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.INVITED_USERS

    @classmethod
    def candidates(cls):
        # CAT 1 :
        # - les invitations à une structure en attente depuis moins de 6 mois
        # - les utilisateurs invités n'ont pas validé leur e-mail
        # filtrée sur les anciens enregistrements (+6 mois)
        return StructurePutativeMember.objects.filter(
            invited_by_admin=True,
            user__is_valid=False,
            creation_date__gt=timezone.now() - relativedelta(months=6),
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
                return notification.created_at + relativedelta(days=20) <= now
            case 5:
                return notification.created_at + relativedelta(days=90) <= now
            case 6:
                return notification.created_at + relativedelta(days=120) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        # plusieurs actions et "cibles" en fonction du temps écoulé
        match notification.counter:
            case 0 | 1 | 2 | 3:
                # relance pour les utilisateurs
                try:
                    send_invitation_reminder(
                        notification.owner_structureputativemember.user,
                        notification.owner_structureputativemember.structure,
                        notification=True,
                    )
                except Exception as ex:
                    raise TaskError(
                        f"Erreur d'envoi de la relance d'invitation ({notification}): {ex}"
                    ) from ex
            case 4:
                # notifications aux administrateurs 20j
                try:
                    send_admin_invited_users_20_notification(
                        notification.owner_structureputativemember.structure,
                        notification.owner_structureputativemember.user,
                    )
                except Exception as ex:
                    raise TaskError(
                        f"Erreur d'envoi de la relance (1) aux administrateurs ({notification}): {ex}"
                    ) from ex
            case 5:
                # notifications aux administrateurs 90j
                try:
                    send_admin_invited_users_90_notification(
                        notification.owner_structureputativemember.structure,
                        notification.owner_structureputativemember.user,
                    )
                except Exception as ex:
                    raise TaskError(
                        f"Erreur d'envoi de la relance (2) aux administrateurs ({notification}): {ex}"
                    ) from ex
            case 6:
                # clôture au préalable de la notification
                notification.complete()

                # action : voir post_process()
            case _:
                raise TaskError(f"Incohérence de compteur ({notification})")

    @classmethod
    def post_process(cls, notification: Notification):
        # cette partie est en "post-process", puisque l'on va détruire le propriétaire de la notification
        # si on effectue cette partie pendant le traitement des tâches,
        # le traitement va planter puisque la notification n'existe plus (détruite en CASCADE).
        if notification.is_complete:
            user = notification.owner_structureputativemember.user

            logger.warning(
                "Suppression d'utilisateur",
                {
                    "legal": True,
                    "userEmail": user.email,
                    "userId": str(user.pk),
                    "structureId": str(
                        notification.owner_structureputativemember.structure.pk
                    ),
                    "reason": "Pas de rattachement à la structure après relances",
                },
            )

            # suppression de l'invitation :
            notification.owner_structureputativemember.delete()
            # à ce point, la notification doit aussi être détruite (CASCADE)...

            # suppression du compte utilisateur associé si :
            # - aucune autre invitation
            # - non membre d'une structure
            if not user.putative_membership.count() and not user.membership.count():
                user.delete()


class SelfInvitedUsersTask(Task):
    @classmethod
    def task_type(cls):
        return TaskType.SELF_INVITED_USERS

    @classmethod
    def candidates(cls):
        # (presque) CAT 2 :
        # - rattachement en attente : l'utilisateur n'a pas été invité par un admin
        # - utilisateurs ayant validé leur adresse e-mail
        return StructurePutativeMember.objects.filter(
            invited_by_admin=False, user__is_valid=True
        )

    @classmethod
    def should_trigger(cls, notification: Notification) -> bool:
        now = timezone.now()

        match notification.counter:
            case 0:
                return notification.created_at + relativedelta(days=1) <= now
            case 1:
                return notification.created_at + relativedelta(days=3) <= now
            case 2:
                return notification.created_at + relativedelta(days=5) <= now
            case 3:
                return notification.created_at + relativedelta(days=7) <= now
            case _:
                return False

    @classmethod
    def process(cls, notification: Notification):
        def _send_email():
            try:
                send_admin_self_invited_users_notification(
                    notification.owner_structureputativemember.structure,
                    notification.owner_structureputativemember.user,
                )
            except Exception as ex:
                raise TaskError(
                    f"Erreur d'envoi de la notification ({notification}): {ex}"
                )

        match notification.counter:
            case 0 | 1 | 2:
                _send_email()
            case 3:
                _send_email()
                notification.complete()
            case _:
                raise TaskError(f"Incohérence de compteur ({notification})")


Task.register(InvitedUsersTask)
Task.register(SelfInvitedUsersTask)
