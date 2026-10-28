from datetime import timedelta
from itertools import chain

from django.core.files.storage import default_storage
from django.utils import timezone

from dora.core.commands import BaseCommand
from dora.core.uploads import iter_managed_objects
from dora.orientations.models import Orientation
from dora.services.models import Service

ORPHAN_AGE_HOURS = 3


class Command(BaseCommand):
    help = f"Supprime les fichiers uploadés orphelins (non référencés en base) de plus de {ORPHAN_AGE_HOURS} heures"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            default=False,
            help="Effectue les suppressions (sinon dry-run)",
        )

    def handle(self, *args, **options):
        wet_run = options["wet_run"]
        cutoff = timezone.now() - timedelta(hours=ORPHAN_AGE_HOURS)

        orientation_paths = set(
            chain.from_iterable(
                Orientation.objects.values_list("beneficiary_attachments", flat=True)
            )
        )

        if not orientation_paths:
            self.logger.error(
                "Abandon : aucun chemin extrait pour les orientations — suppression annulée par sécurité."
            )
            return

        # `Service.objects` masque les modèles (`is_model=True`), qui portent eux aussi des
        # documents : le gestionnaire de base les inclut.
        service_form_paths = set(
            chain.from_iterable(Service._base_manager.values_list("forms", flat=True))
        )

        if not service_form_paths:
            self.logger.error(
                "Abandon : aucun chemin extrait pour les services — suppression annulée par sécurité."
            )
            return

        documents_to_keep = orientation_paths | service_form_paths

        deleted = 0
        skipped_recent = 0
        skipped_referenced = 0

        for file_path, last_modified in iter_managed_objects():
            if file_path in documents_to_keep:
                skipped_referenced += 1
                continue

            if last_modified > cutoff:
                skipped_recent += 1
                continue

            if wet_run:
                try:
                    default_storage.delete(file_path)
                    deleted += 1
                    self.logger.info("Supprimé: %s", file_path)
                except Exception as e:
                    self.logger.warning(
                        "Erreur lors de la suppression de %s: %s", file_path, e
                    )
            else:
                self.logger.info("[dry-run] Serait supprimé: %s", file_path)
                deleted += 1

        self.logger.info(
            "%d fichiers %s, %d récents ignorés, %d référencés ignorés.",
            deleted,
            "supprimés" if wet_run else "seraient supprimés",
            skipped_recent,
            skipped_referenced,
        )
