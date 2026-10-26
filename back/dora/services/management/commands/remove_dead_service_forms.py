"""Retire de `Service.forms` les documents dont l'objet n'existe plus dans le bucket.

Le nettoyage des fichiers orphelins (`delete_orphaned_uploads`) ignorait les modèles de
service : il a supprimé les documents référencés seulement par un modèle, que les
services créés ou synchronisés depuis ce modèle ont ensuite recopiés. Faute de
versioning et de sauvegarde du bucket, ces fichiers sont perdus ; leurs références ne
produisent plus que des liens de téléchargement en 404.

Seules les clés gérées par le nettoyage (`_MANAGED_KEY`) sont examinées. Les services
sont lus avant le bucket : un document est envoyé avant d'être référencé, donc toute clé
lue en base existe déjà au moment où le bucket est listé.

Sans `--wet-run`, rien n'est écrit : la commande se contente de journaliser ce qu'elle
ferait.
"""

from dora.core.commands import BaseCommand
from dora.core.management.commands.delete_orphaned_uploads import (
    _MANAGED_KEY,
    _iter_objects,
)
from dora.services.models import Service
from dora.services.utils import save_forms


class Command(BaseCommand):
    help = "Retire de `Service.forms` les documents absents du bucket"

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            default=False,
            help="Effectue les modifications (sinon dry-run)",
        )

    def handle(self, *args, **options):
        wet_run = options["wet_run"]

        # `Service.objects` masque les modèles (`is_model=True`), qui portent eux aussi des
        # documents : le gestionnaire de base les inclut.
        services = list(Service._base_manager.exclude(forms=[]))

        existing = {key for key, _ in _iter_objects()}
        if not existing:
            self.logger.error(
                "Abandon : aucun objet listé dans le bucket — modification annulée par sécurité."
            )
            return

        cleaned = []
        removed_count = 0

        for service in services:
            dead = [
                form
                for form in service.forms
                if _MANAGED_KEY.match(form) and form not in existing
            ]
            if not dead:
                continue

            removed_count += len(dead)
            self.logger.info(
                "%s %s : %d document(s) %s : %s",
                "Modèle" if service.is_model else "Service",
                service.slug,
                len(dead),
                "retiré(s)" if wet_run else "seraient retiré(s)",
                ", ".join(dead),
            )

            service.forms = [form for form in service.forms if form not in dead]
            cleaned.append(service)

        checksums_updated = save_forms(cleaned, wet_run)

        self.logger.info(
            "%d document(s) %s sur %d service(s), %d empreinte(s) de modèle %s.",
            removed_count,
            "retiré(s)" if wet_run else "seraient retiré(s)",
            len(cleaned),
            checksums_updated,
            "recalculée(s)" if wet_run else "seraient recalculée(s)",
        )
