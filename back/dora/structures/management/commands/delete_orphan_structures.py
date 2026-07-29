from datetime import datetime
from zoneinfo import ZoneInfo

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.structures.models import Structure

CREATED_BEFORE = datetime(2026, 2, 1, tzinfo=ZoneInfo("Europe/Paris"))


def get_orphan_structures():
    # structures créées avant la date limite, sans aucun utilisateur (ni membre,
    # ni membre potentiel), sans service (les modèles de service sont des
    # `Service` en base) et dont l'administrateur n'a jamais été invité.
    # Deux garde-fous supplémentaires :
    # - les structures mères sont exclues, leur suppression entrainerait en
    #   cascade celle de leurs antennes, qui peuvent, elles, être actives ;
    # - les structures possédant des choix personnalisés (`accesscondition`,
    #   `public`, `requirement`, `credential`) sont exclues, ces derniers pouvant
    #   être utilisés par les services d'autres structures.
    return Structure.objects.filter(
        creation_date__lt=CREATED_BEFORE,
        membership=None,
        putative_membership=None,
        services=None,
        branches=None,
        admin_already_invited=False,
        accesscondition=None,
        public=None,
        requirement=None,
        credential=None,
    )


class Command(AtomicHandleMixin, BaseCommand):
    help = (
        "Supprime les structures orphelines, sans service, jamais activées, "
        f"créées avant le {CREATED_BEFORE:%d/%m/%Y}"
    )
    ATOMIC_HANDLE = True

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            help="Exécute réellement les suppressions (sans ce flag, rollback automatique).",
        )

    @dry_runnable
    def handle(self, *args, **options):
        # suppression via le queryset de `Structure` : la synchronisation Nexus
        # est déclenchée sur le commit, donc ignorée en cas de dry run
        total, per_model = get_orphan_structures().delete()

        self.logger.info("%d objets supprimés :", total)
        for label, count in sorted(per_model.items()):
            self.logger.info("  %s : %d", label, count)
