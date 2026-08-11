from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.models import Service
from dora.services.utils import compute_service_kind

BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    """Réconcilie `Service.kind` avec la M2M historique `Service.kinds`.

    La double écriture (`dora.services.signals_kind`) suffit en régime nominal ; cette commande
    rattrape les divergences éventuelles (écriture SQL directe, restauration de base) et permet
    de rejouer le calcul après un changement de l'ordre de priorité.
    """

    help = "Réconcilie le type de service `kind` avec la M2M historique `kinds`"
    ATOMIC_HANDLE = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Écrit réellement les corrections (sans ce flag, rollback automatique).",
        )

    @dry_runnable
    def handle(self, *args, **options):
        total = Service._base_manager.count()
        self.logger.info("%d services et modèles de service à vérifier", total)

        mismatches = 0
        updated = []
        qs = (
            Service._base_manager.exclude(kinds__isnull=True, kind__isnull=True)
            .prefetch_related("kinds")
            .only("pk", "kind")
            .iterator(chunk_size=BATCH)
        )
        for service in qs:
            kind = compute_service_kind(service)
            if service.kind == kind:
                continue

            mismatches += 1
            self.logger.info("%s : %r -> %r", service.pk, service.kind, kind)

            service.kind = kind
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["kind"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["kind"])

        self.logger.info("%d services corrigés", mismatches)
