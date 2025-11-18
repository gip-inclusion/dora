import logging
import time

from django.conf import settings

from dora.core.commands import BaseCommand
from dora.notifications.tasks.core import Task

"""
Lancement / activation des notifications :
    - récupère la liste des tâches actuellement enregitrées
    - effectue un `run()` sur chaque tâche (rafraichissement, purge, et actions)

Limite d'enregistrements à traiter possible et dry-run par défaut.

Le système peut être activé ou limité dynamiquement par l'utilisation de variables
d'environnement sur l'environnement cible :
    - NOTIFICATIONS_ENABLED    : notifications activées seulement si `true` (par défaut: non)
    - NOTIFICATIONS_TASK_TYPES : sélectionne les notifications à lancer, équivalent de `--types` (défaut: tous les types activés)
    - NOTIFICATIONS_LIMIT      : nombre limite de notifications traitées en une fois pour chaque tâche (défaut: 0, pas de limite)

Ces variables sont définies dans les `settings` de Django.
"""

logger = logging.getLogger("dora.logs.core")


class Command(BaseCommand):
    help = "Lancement des tâches de notification"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Par défaut les taches sont seulement listées, pas executées. Ce paramètre active le traitement effectif des tâches.",
        )
        parser.add_argument(
            "--limit",
            type=int,
            help="Limite du nombre de tâches à traiter",
            default=settings.NOTIFICATIONS_LIMIT,
        )

        # FIXME:
        # si on inclut directement la valeur de `possible_tasks` dans la f-string ci-dessous,
        # ruff formattera le fichier au format python 3.12 (menant à une erreur sur python 3.11)
        # impossible de forcer un formattage compatible python 3.11 à cette heure (même avec `target-version`)
        # cause : voir https://docs.python.org/3/whatsnew/3.12.html#pep-701-syntactic-formalization-of-f-strings
        possible_tasks = "|".join(
            [task.task_type() for task in Task.registered_tasks()]
        )

        parser.add_argument(
            "--types",
            type=str,
            help=(
                f"Types de tâche de notification à prendre en compte, séparés par ','"
                f" ({possible_tasks})"
            ),
            default=settings.NOTIFICATIONS_TASK_TYPES,
        )

        parser.add_argument(
            "--force",
            action="store_true",
            help="Force l'activation des notifications sans tenir compte de 'settings.NOTIFICATIONS_ENABLED'. Utile pour un lancement manuel.",
        )

    def handle(self, *args, **options):
        force = options["force"]

        if not (settings.NOTIFICATIONS_ENABLED or force):
            self.stdout.write(
                self.style.WARNING(
                    "Le système de notification n'est pas activé sur cet environnement."
                )
            )
            return

        wet_run = options["wet_run"]
        limit = options["limit"]
        types = options["types"]

        if wet_run:
            self.stdout.write(self.style.WARNING("PRODUCTION RUN"))
        else:
            self.stdout.write(self.style.NOTICE("DRY-RUN"))
            self.stdout.write(
                self.style.WARNING(
                    " - les notifications ne sont pas créées dans ce mode"
                )
            )

        if force:
            self.stdout.write(
                self.style.NOTICE(" - activation FORCÉE des notifications\n")
            )

        if types:
            self.stdout.write(
                self.style.WARNING(f" - tâche(s) sélectionnée(s) : {types}")
            )

        if limit:
            self.stdout.write(
                self.style.WARNING(f" - limite de notifications par tâche : {limit}")
            )

        self.stdout.write()

        if not Task.registered_tasks():
            self.stdout.write(" > aucune tâche enregistrée !")
            return

        # Par défaut, tous les types de tâches enregistrés sont sélectionnés
        selected_types = Task.registered_tasks()

        if types:
            selected_types = [
                task
                for task in Task.registered_tasks()
                if task.task_type() in types.split(",")
            ]

        if not selected_types:
            self.stdout.write(
                self.style.WARNING(
                    "Aucun type de tâche de notification sélectionné : fin du traitement"
                )
            )
            return

        total_timer = 0

        for task_class in selected_types:
            task = task_class()

            self.stdout.write(
                self.style.NOTICE(
                    f"> {task_class.__name__} ({task_class.task_type()}) :"
                )
            )
            self.stdout.write(
                self.style.WARNING(
                    f" > nombre d'éléments candidats : {len(task.candidates())}"
                )
            )

            timer = time.time()
            ok, errors, obsolete = task.run(
                strict=True, dry_run=not wet_run, limit=limit
            )
            timer = time.time() - timer

            if ok:
                self.stdout.write(
                    self.style.SUCCESS(
                        f" > {ok} notification(s) traitée(s) en {timer:.2f}s"
                    )
                )
                total_timer += timer
            else:
                self.stdout.write(" > aucune notification traitée")

            if errors:
                self.stdout.write(
                    self.style.ERROR(f" > {errors} notification(s) en erreur")
                )
            else:
                self.stdout.write(" > aucune erreur")

            if obsolete:
                self.stdout.write(
                    self.style.SUCCESS(
                        f" > {obsolete} notification(s) obsolètes modifiées"
                    )
                )
            else:
                self.stdout.write(" > aucune notification obsolète")

            self.stdout.write()

            if wet_run:
                logger.info(
                    f"process_notification_tasks:{task_class.task_type()}",
                    {
                        "taskType": task_class.task_type(),
                        "nbCandidates": len(task.candidates()),
                        "nbProcessed": ok,
                        "nbObsolete": obsolete,
                        "nbErrors": errors,
                        "processingTimeSecs": round(timer, 2),
                    },
                )

        self.stdout.write(self.style.NOTICE(f"Terminé en {total_timer:.2f}s !"))
