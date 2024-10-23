import abc

from django.db import models

from dora.notifications.enums import NotificationStatus, TaskType
from dora.notifications.models import Notification

"""
Tasks:
    Les tâches de notification étendent cette classe, et doivent implémenter les fonctions :
        - `task_type` : le tag qui permet de rattacher les notifications en base à un type de tâche,
        - `candidates` : retourne un `queryset` contenant la liste des objets concernés par la tâche,
        - `should_trigger` : contient l'implémentation de la planification de la tâche,
        - `process` : enrobe l'action à effectuer si une notification est déclenchée.

    `run` effectue principalement 3 opérations :
        - marquage des notifications obsolètes : pour les objets qui ne sont plus des "candidats",
        - création des nouvelles notifications : en vérifiant si il existe toujours une
          notification en attente pour les objets candidat concernés,
        - vérification du déclenchement des notifications et lancement de l'action associée.

    Il est possible d'enregistrer les classes de tâche via `register` pour que la management command
    `process_notification_tasks` la prenne automatiquement en compte.
"""


class TaskError(Exception):
    pass


class Task(abc.ABC):
    _registered_tasks = set()

    @classmethod
    @abc.abstractmethod
    def task_type(cls) -> TaskType:
        # type de la tâche : déclaré dans `enums.TaskType`
        pass

    @classmethod
    @abc.abstractmethod
    def candidates(cls) -> list:
        # liste des objets concernés par cette tâche de notification
        pass

    @classmethod
    @abc.abstractmethod
    def should_trigger(cls, notification: Notification) -> bool:
        # indique si cette notification doit être déclenchée (code)
        pass

    @classmethod
    @abc.abstractmethod
    def process(cls, notification: Notification):
        # précise quelle est l'action à effectuer pour un type de notification donné
        pass

    @classmethod
    def post_process(cls, notification: Notification):
        # précise quelle est l'action à effectuer *après* le traitement pour une notification donnée
        # peut être utile si on essaye de supprimer des èléments comme le propriétaire lors d'une action
        pass

    def __init__(self, *args, limit=None, **kwargs):
        # le type de l'objet à récupérer est déduit du nom de la FK
        model_key = f"owner_{self.candidates().model.__name__}_id".lower()

        if model_key not in Notification.__dict__:
            raise TaskError(
                f"Le champ '{model_key}' n'existe pas dans le modèle de notification"
            )

        self._model_key = model_key

    def _check(self, notification: Notification) -> Notification:
        # permet, au besoin, de vérifier l'état de la notification avant traitement
        if not notification:
            raise TaskError("Notification invalide")

        if notification.task_type != self.task_type():
            raise TaskError(
                f"Type de notification incompatible : {notification.task_type}"
            )

        if not notification.is_pending:
            raise TaskError(
                f"Cette notification n'est pas en attente de traitement : {notification}"
            )

        ...

        return notification

    def _new_notification(cls, owner, **kwargs) -> Notification:
        if not owner:
            raise TaskError("Pas de propriétaire défini")

        n = Notification(task_type=cls.task_type(), **kwargs)
        owner_field = f"owner_{type(owner).__name__}".lower()

        if not hasattr(n, owner_field):
            raise TaskError(
                f"Le modèle de notification n'a pas de champ nommé '{owner_field}'"
            )

        setattr(n, owner_field, owner)

        return n

    def _create_run_querysets(self) -> tuple[models.QuerySet, models.QuerySet]:
        # création des querysets nécessaires à l'execution
        # le plus tard possible pour éviter des modifications entre
        # la création de la tâche et l'exécution proprement dites
        current_candidates = self.candidates()

        # liste des objets déjà rattachés à une notification active :
        notifications_already_created = Notification.objects.filter(
            task_type=self.task_type()
        )
        objects_with_notification = models.QuerySet(
            model=current_candidates.model
        ).filter(
            pk__in=notifications_already_created.values_list(self._model_key, flat=True)
        )

        # liste des objets non concernés par une notification :
        obsolete_objects = objects_with_notification.difference(
            current_candidates
        ).values_list("pk", flat=True)
        # le queryset est filtré dynamiquement sur le type de modèles des objets candidats
        # on ne garde que les notifications actives
        diff = {self._model_key + "__in": obsolete_objects}
        obsolete_notifications = notifications_already_created.pending().filter(**diff)

        # notifications à créer pour les nouveaux candidats :
        new_candidates = [
            self._new_notification(obj)
            for obj in current_candidates.difference(objects_with_notification)
        ]

        # - les notifications devant être créées
        # - les notifications actuellement obsolètes (à clore)
        return new_candidates, obsolete_notifications

    def run(
        self, *, strict=True, dry_run=False, limit=None, **kwargs
    ) -> tuple[int, int, int]:
        # - `strict`: lève une exception à la première erreur de traitement (par défaut)
        # - `dry_run`: un tour pour pour rien
        # - `limit` : nombre de notifications à traiter (toutes par défaut)
        # retourne le nombre de notifications correctement traitées, en erreur et obsolètes
        if limit is not None:
            if not isinstance(limit, int):
                raise TaskError("'limit' doit être entier")

        # récupération des différentes données à traiter :
        new_candidates, obsolete_notifications = self._create_run_querysets()
        errors = ok = nb_obsolete = 0

        if not dry_run:
            # clôture des notifications obsolètes
            if obsolete_notifications:
                nb_obsolete = obsolete_notifications.update(
                    status=NotificationStatus.COMPLETE
                )

            # création des nouvelles notifications
            if new_candidates:
                Notification.objects.bulk_create(new_candidates)

        # traitement des notifications actives et en attente :
        notifications = (
            Notification.objects.pending()
            .filter(task_type=self.task_type())
            .order_by("updated_at")
        )

        # notifications ordonnées par date de maj en cas d'utilisation de la limite
        notifications = notifications[:limit] if limit else notifications

        for n in notifications:
            if self.should_trigger(n):
                try:
                    if not dry_run:
                        self.process(self._check(n))
                except Exception as ex:
                    if strict:
                        # mode strict (par défaut) : on sort à la première exception
                        raise TaskError(
                            f"Erreur d'exécution de l'action pour : {n}"
                        ) from ex
                    errors += 1
                else:
                    if not dry_run:
                        # si tout s'est bien passé, on marque la notification comme ayant
                        # été activée (incrément du compteur)
                        n.trigger()

                        # traitement à posteriori
                        self.post_process(n)
                    ok += 1

        # (traitées correctement, en erreur, obsolètes / objet candidat sorti du scope)
        return ok, errors, nb_obsolete

    @classmethod
    def register(cls, class_):
        if not (class_ and issubclass(class_, Task)):
            raise TaskError("Impossible d'enregistrer cette classe")

        cls._registered_tasks.add(class_)

    @classmethod
    def unregister(cls, class_):
        if not class_ or class_ not in cls._registered_tasks:
            raise TaskError("Impossible de retirer cette classe")

        cls._registered_tasks.remove(class_)

    @classmethod
    def registered_tasks(cls) -> set["Task"]:
        return cls._registered_tasks
