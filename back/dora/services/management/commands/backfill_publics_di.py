from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.models import Service
from dora.services.utils import compute_publics_di

BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    ATOMIC_HANDLE = True
    help = "Réconciliation des services dont les publics ont divergé de leurs valeurs pour les colonnes publics_di"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
        )

    @dry_runnable
    def handle(self, *args, **options):
        total = Service._base_manager.count()
        self.stdout.write(
            self.style.NOTICE(f"{total} services et modèles de service à vérifier")
        )

        mismatches = 0
        updated = []
        qs = (
            Service._base_manager.prefetch_related("publics")
            .only("pk", "publics_di")
            .iterator(chunk_size=BATCH)
        )
        for service in qs:
            publics_di = compute_publics_di(service)
            if service.publics_di == publics_di:
                continue

            mismatches += 1
            self.stdout.write(
                f"{service.pk}: {service.publics_di!r} -> {publics_di!r} | "
            )

            service.publics_di = publics_di
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["publics_di"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["publics_di"])

        if options["wet_run"]:
            self.stdout.write(self.style.SUCCESS(f"{mismatches} services corrigés"))
        else:
            self.stdout.write(
                self.style.WARNING(f"{mismatches} services à corriger (dry-run)")
                if mismatches
                else self.style.SUCCESS("Aucun écart : colonnes synchronisées")
            )
