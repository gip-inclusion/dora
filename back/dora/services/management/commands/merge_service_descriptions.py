"""Réintégration du résumé des services dans leur description, le temps de la migration.

Sans `--from-csv`, applique les cas évidents et exporte les couples restants, à fusionner par
un LLM (`--show-prompt`) ; avec, applique les fusions obtenues. Les services modifiés entre
les deux passages repartent dans l'export plutôt que d'être écrasés par une fusion périmée.
"""

import csv
import hashlib
from datetime import datetime

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.core.utils import strip_markdown
from dora.services.models import Service
from dora.services.utils import (
    SYNC_CUSTOM_M2M_FIELDS,
    SYNC_M2M_FIELDS,
    update_sync_checksum,
)

BATCH = 500

FIELDNAMES = ["pair_hash", "nb_services", "short_desc", "description"]

PROMPT = """\
Fusionne deux champs d'une fiche de service d'insertion : un résumé court et une
description. Le résultat remplacera les deux.

Règles :
- La description est le texte de référence : reproduis-la à l'identique. Pas de reformulation,
  pas de correction de style ou d'orthographe, pas de réorganisation, pas de titre ajouté.
- Si le résumé n'apporte aucune information absente de la description, renvoie la description
  telle quelle, sans rien y changer.
- S'il apporte une information absente, insère-la — en tête par défaut, ou à l'endroit
  pertinent — en une phrase courte, dans le ton du texte existant.
- N'invente rien, ne complète pas, ne développe pas.
- Réponds par la description seule, en Markdown, sans préambule ni commentaire.
"""


def needs_merge(short_desc: str, description: str) -> bool:
    """Le résumé apporte-t-il quelque chose que la description ne dit pas déjà ?"""
    # `strip_markdown` ramène le texte sur une seule ligne, ce qui rend comparables un résumé
    # saisi en texte brut et un descriptif mis en forme.
    short_desc = strip_markdown(short_desc).strip().lower()
    return bool(short_desc) and short_desc not in strip_markdown(description).lower()


def pair_hash(short_desc: str, description: str) -> str:
    """Empreinte d'un couple de valeurs brutes, clé de correspondance des deux CSV.

    C'est l'égalité stricte qui garantit qu'un modèle et ses copies reçoivent la même fusion.
    """
    digest = hashlib.sha256(
        repr((short_desc, description)).encode(), usedforsecurity=False
    )
    return digest.hexdigest()[:16]


class Command(AtomicHandleMixin, BaseCommand):
    ATOMIC_HANDLE = True
    help = (
        "Réintègre le résumé des services dans leur description : copie directe quand la "
        "description est vide, fusions calculées par un LLM avec --from-csv. Les couples "
        "restant à fusionner sont exportés en CSV."
    )

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")
        parser.add_argument(
            "--from-csv",
            type=str,
            help="CSV de fusions (colonnes `pair_hash` et `description`)",
        )
        parser.add_argument(
            "--output",
            type=str,
            help="CSV des couples restant à fusionner (par défaut : nom horodaté)",
        )
        parser.add_argument(
            "--show-prompt",
            action="store_true",
            help="Affiche la consigne de fusion à donner au LLM, et sort",
        )

    @dry_runnable
    def handle(self, *args, **options):
        if options["show_prompt"]:
            self.stdout.write(PROMPT)
            return

        merges = self._load_merges(options["from_csv"]) if options["from_csv"] else {}
        updated, touched_models, pending = [], set(), {}
        copied = applied = 0

        # `_base_manager` pour inclure les modèles
        services = (
            Service._base_manager.only("pk", "is_model", "short_desc", "description")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for service in services:
            short_desc, description = service.short_desc.strip(), service.description
            if not short_desc or not needs_merge(short_desc, description):
                continue

            if not description.strip():
                service.description = short_desc
                copied += 1
            else:
                key = pair_hash(service.short_desc, description)
                if key not in merges:
                    pending.setdefault(
                        key,
                        {
                            "pair_hash": key,
                            "nb_services": 0,
                            "short_desc": service.short_desc,
                            "description": description,
                        },
                    )["nb_services"] += 1
                    continue

                service.description = merges[key]
                applied += 1

            if service.is_model:
                touched_models.add(service.pk)
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["description"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["description"])

        self.stdout.write(f"{copied:>7} descriptions reprises du résumé")
        self.stdout.write(f"{applied:>7} descriptions fusionnées depuis le CSV")
        self.stdout.write(f"{len(pending):>7} couples restant à fusionner")
        if pending:
            self._write_pending(pending, options["output"])

        self.stdout.write(
            f"{self._recompute_sync_checksums(touched_models):>7} empreintes recalculées"
        )
        if not options["wet_run"]:
            self.stdout.write(
                self.style.WARNING("Dry-run : aucune modification enregistrée")
            )

    def _load_merges(self, path: str) -> dict[str, str]:
        with open(path, encoding="utf-8", newline="") as csv_file:
            return {
                row["pair_hash"]: row["description"].strip()
                for row in csv.DictReader(csv_file)
                if row["description"].strip()
            }

    def _write_pending(self, pending: dict[str, dict], path: str | None):
        path = path or f"descriptions_{datetime.now():%Y%m%d_%H%M%S}.csv"
        with open(path, "w", encoding="utf-8", newline="") as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
            writer.writeheader()
            writer.writerows(pending.values())
        self.stdout.write(self.style.NOTICE(f"Couples à fusionner écrits dans {path}"))

    def _recompute_sync_checksums(self, model_ids: set) -> int:
        recomputed = 0
        updated = []
        models = (
            Service._base_manager.filter(pk__in=model_ids)
            .prefetch_related(*SYNC_M2M_FIELDS, *SYNC_CUSTOM_M2M_FIELDS)
            .iterator(chunk_size=BATCH)
        )
        for model in models:
            previous = model.sync_checksum
            model.sync_checksum = update_sync_checksum(model)
            if model.sync_checksum == previous:
                continue

            Service._base_manager.filter(
                model_id=model.pk, last_sync_checksum=previous
            ).update(last_sync_checksum=model.sync_checksum)

            recomputed += 1
            updated.append(model)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["sync_checksum"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["sync_checksum"])

        return recomputed
