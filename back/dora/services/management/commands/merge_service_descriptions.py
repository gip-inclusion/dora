"""Composition initiale de la description dérivée des services.

`Service.save()` la recompose à chaque enregistrement, mais les services que personne n'a
touchés depuis le déploiement l'ont vide : cette commande les rattrape. Elle ne touche qu'au
champ dérivé, et peut donc être rejouée. Elle pèse en outre les mots par leur rareté dans le
corpus des descriptifs, ce qu'un enregistrement, qui ne voit qu'un service, ne peut pas faire.
"""

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.descriptions import build_idf, is_blank, merge_description
from dora.services.models import Service

BATCH = 500


class Command(AtomicHandleMixin, BaseCommand):
    ATOMIC_HANDLE = True
    help = (
        "Compose la description dérivée des services : le résumé en tête du descriptif "
        "quand il le complète, abandonné quand il ne fait que le redire."
    )

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")

    @dry_runnable
    def handle(self, *args, **options):
        weight = build_idf(
            Service._base_manager.exclude(full_desc="")
            .values_list("full_desc", flat=True)
            .iterator(chunk_size=BATCH)
        )

        updated = []
        composed = copied = dropped = written = 0

        services = (
            Service._base_manager.only("pk", "short_desc", "full_desc", "description")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for service in services:
            merged = merge_description(service.short_desc, service.full_desc, weight)
            if merged is None:
                # Le résumé n'apporte rien, ou n'existe pas.
                if not is_blank(service.short_desc):
                    dropped += 1
                description = service.full_desc
            elif is_blank(service.full_desc):
                copied += 1
                description = merged
            else:
                composed += 1
                description = merged

            if description == service.description:
                continue

            service.description = description
            written += 1
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["description"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["description"])

        self.stdout.write(f"{composed:>7} résumés repris en tête du descriptif")
        self.stdout.write(f"{copied:>7} descriptions tirées du seul résumé")
        self.stdout.write(
            f"{dropped:>7} résumés abandonnés, déjà dits par le descriptif"
        )
        self.stdout.write(f"{written:>7} descriptions écrites")
        if not options["wet_run"]:
            self.stdout.write(
                self.style.WARNING("Dry-run : aucune modification enregistrée")
            )
