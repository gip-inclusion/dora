"""Retire les documents référencés deux fois par un même service.

Deux entrées identiques de `Service.forms` désignent le même objet stocké : le serveur
range les documents d'une structure sous une clé dérivée de leur nom (`ENV/<structure>/
<nom>`) et `S3Storage` écrase l'objet existant, si bien qu'un second envoi du même nom
renvoie la clé déjà présente. Les retirer ne fait donc perdre aucun document.

Deux clés *distinctes* portant le même nom de fichier sont un autre cas : elles désignent
bien deux objets différents (une copie de modèle porte les clés de la structure du modèle,
préfixées par un autre identifiant). La commande les signale sans y toucher — les
départager demande de savoir lequel garder, ce qui n'appartient pas à un traitement
automatique. Ces services resteront refusés par `validate_unique_form_names` à leur
prochain enregistrement, tant qu'un humain n'aura pas tranché.

Sans `--wet-run`, rien n'est écrit : la commande se contente de journaliser ce qu'elle
ferait.
"""

from dora.core.commands import BaseCommand
from dora.services.models import Service
from dora.services.utils import update_sync_checksum

BATCH = 500


def file_name(key):
    return key.rsplit("/", 1)[-1]


class Command(BaseCommand):
    help = (
        "Retire les doublons exacts de `Service.forms` et signale les clés distinctes "
        "partageant un nom de fichier"
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--wet-run",
            action="store_true",
            default=False,
            help="Effectue les modifications (sinon dry-run)",
        )

    def handle(self, *args, **options):
        wet_run = options["wet_run"]

        deduplicated = []
        removed_count = 0
        collision_count = 0

        # `Service.objects` masque les modèles (`is_model=True`), qui portent eux aussi des
        # documents : le gestionnaire de base les inclut.
        services = Service._base_manager.exclude(forms=[]).iterator(chunk_size=BATCH)
        for service in services:
            seen_keys = set()
            kept = []
            removed = []
            for form in service.forms:
                if form in seen_keys:
                    removed.append(form)
                    continue
                seen_keys.add(form)
                kept.append(form)

            keys_by_name = {}
            for form in kept:
                keys_by_name.setdefault(file_name(form), []).append(form)

            for name, keys in sorted(keys_by_name.items()):
                if len(keys) > 1:
                    collision_count += 1
                    self.logger.warning(
                        "Service %s : %d documents distincts nommés « %s », laissés en "
                        "l'état : %s",
                        service.slug,
                        len(keys),
                        name,
                        ", ".join(keys),
                    )

            if not removed:
                continue

            removed_count += len(removed)
            self.logger.info(
                "Service %s : %d doublon(s) %s : %s",
                service.slug,
                len(removed),
                "retiré(s)" if wet_run else "seraient retiré(s)",
                ", ".join(removed),
            )

            service.forms = kept
            deduplicated.append(service)

        checksums_updated = self.update_forms(deduplicated, wet_run)

        self.logger.info(
            "%d doublon(s) %s sur %d service(s), %d empreinte(s) de modèle %s, "
            "%d collision(s) de noms signalée(s).",
            removed_count,
            "retiré(s)" if wet_run else "seraient retiré(s)",
            len(deduplicated),
            checksums_updated,
            "recalculée(s)" if wet_run else "seraient recalculée(s)",
            collision_count,
        )

    def update_forms(self, deduplicated, wet_run):
        """Écrit les listes dédoublonnées et réaligne les empreintes des modèles touchés.

        `forms` entre dans l'empreinte de synchronisation : sans recalcul, l'empreinte
        stockée d'un modèle resterait celle d'avant le dédoublonnage, et son prochain
        enregistrement ferait basculer d'un coup toutes ses copies en « modèle modifié ».
        Les copies encore à jour suivent la nouvelle empreinte ; celles qui divergeaient
        déjà gardent la leur, pour ne pas masquer des modifications en attente.
        """
        checksums_updated = 0
        models = []

        for service in deduplicated:
            if not service.is_model:
                continue

            previous = service.sync_checksum
            service.sync_checksum = update_sync_checksum(service)
            if service.sync_checksum == previous:
                continue

            checksums_updated += 1
            models.append(service)

            if not wet_run:
                continue

            Service._base_manager.filter(
                model_id=service.pk, last_sync_checksum=previous
            ).update(last_sync_checksum=service.sync_checksum)

        if wet_run:
            for start in range(0, len(deduplicated), BATCH):
                Service._base_manager.bulk_update(
                    deduplicated[start : start + BATCH], ["forms"]
                )
            for start in range(0, len(models), BATCH):
                Service._base_manager.bulk_update(
                    models[start : start + BATCH], ["sync_checksum"]
                )

        return checksums_updated
