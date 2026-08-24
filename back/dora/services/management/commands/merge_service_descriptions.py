"""Réintégration du résumé des services dans leur description, le temps de la migration.

`Service.short_desc` disparaît au profit d'une description unique. Certains résumés complètent
la description — à conserver, en tête — et d'autres n'en sont qu'une recopie ou une paraphrase
— à jeter.

Aucun texte n'est jamais réécrit : `normalize` ne sert qu'à comparer, jamais à produire, ce qui
met la typographie du texte de référence hors d'atteinte.
"""

import difflib
import math
import re
import unicodedata
from collections import Counter
from functools import lru_cache
from typing import Callable, Iterable

from itoutils.django.commands import AtomicHandleMixin, dry_runnable

from dora.core.commands import BaseCommand
from dora.services.models import Service
from dora.services.utils import (
    SYNC_CUSTOM_M2M_FIELDS,
    SYNC_M2M_FIELDS,
    update_sync_checksum,
)

BATCH = 500

# Deux mesures, parce qu'elles attrapent des redondances de nature différente et se rattrapent
# l'une l'autre : l'ordonnée tranche la recopie fautive, que la pondération par rareté prend
# au contraire pour un apport — une faute de frappe fabrique un mot rare ; la désordonnée
# tranche la paraphrase, qui réordonne les mots, et absorbe les flexions que l'ordonnée rate.
SEQUENCE_THRESHOLD = 0.90
BAG_THRESHOLD = 0.90

# Racines tronquées à cette longueur : « accompagnement » et « accompagnons » doivent compter
# pour le même mot, sans embarquer de lemmatiseur.
STEM_LENGTH = 5

# Mots-outils écartés de la comparaison désordonnée. L'appartenance est testée sur le mot
# entier, avant troncature : « entre » emporterait « entreprise », « entretien » et
# « entreprendre ». Les mots d'une ou deux lettres n'y figurent pas, `stems` les écarte déjà.
STOPWORDS = set(
    """
    les une des aux mais donc car que qui quoi dont
    cet cette ces son ses leur leurs notre nos votre vos mon mes ton tes
    elle nous vous ils elles
    est sont etre suis sommes etes ete etait etaient sera seront soit
    avoir avons avez ont avait avaient
    pour par sur sous dans avec sans vers chez entre depuis pendant afin ainsi aussi
    plus moins tres tout tous toute toutes meme autre autres chaque
    pas non oui comme lors alors apres avant
    peut peuvent pouvez pouvons permet permettre fait faire faites
    cela ceux celle celles etc
    """.split()
)

APOSTROPHES = re.compile(r"['‘’ʼ`]")
NON_ALPHANUMERIC = re.compile(r"[^a-z0-9]+")


def normalize(text: str) -> list[str]:
    """Mots comparables : casse, accents, ponctuation et balisage effacés.

    Volontairement destructeur — c'est ce qui reconnaît « l'Accueil » dans « L’accueil ».
    """
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return NON_ALPHANUMERIC.sub(" ", APOSTROPHES.sub(" ", text)).split()


def is_blank(text: str) -> bool:
    """Le texte se réduit-il à de la ponctuation ou du balisage — « --- », « *** », « ... » ?"""
    return not normalize(text)


def stems(words: Iterable[str]) -> set[str]:
    """Racines porteuses de sens d'une suite de mots.

    Les nombres comptent quelle que soit leur longueur : un âge ou un nombre de places est
    souvent tout ce qu'un résumé ajoute à une description qui n'en dit rien.
    """
    return {
        word[:STEM_LENGTH]
        for word in words
        if (word.isdigit() or len(word) > 2) and word not in STOPWORDS
    }


def uniform_weight(stem: str) -> float:
    """Pondération neutre, quand aucun corpus n'est disponible pour en tirer une."""
    return 1.0


def build_idf(descriptions: Iterable[str]) -> Callable[[str], float]:
    """Poids de rareté d'une racine, tiré du corpus des descriptions.

    Sans elle, le vocabulaire omniprésent du secteur — « accompagnement », « insertion » —
    ferait passer pour une paraphrase un résumé qui apporte du neuf.
    """
    document_frequency = Counter()
    total = 0
    for description in descriptions:
        total += 1
        document_frequency.update(stems(normalize(description)))

    if not total:
        return uniform_weight

    def weight(stem: str) -> float:
        # `1 + N / (1 + df)` reste strictement positif même pour une racine présente partout,
        # là où le `N / (1 + df)` habituel passerait sous zéro.
        return math.log(1 + total / (1 + document_frequency[stem]))

    return weight


def sequence_coverage(short_desc: str, description: str) -> float:
    """Part du résumé retrouvée *dans l'ordre* dans la description : la recopie."""
    words = normalize(short_desc)
    matcher = difflib.SequenceMatcher(a=words, b=normalize(description), autojunk=False)
    # Les blocs d'un seul mot ne sont que des mots-outils tombés au bon endroit : dans une
    # description longue, ils suffiraient à faire passer n'importe quel résumé pour une recopie.
    matched = sum(
        block.size for block in matcher.get_matching_blocks() if block.size >= 2
    )
    return matched / len(words)


def bag_coverage(
    short_desc: str, description: str, weight: Callable[[str], float]
) -> float:
    """Part du résumé retrouvée *sans égard à l'ordre*, pondérée par la rareté : la paraphrase."""
    summary = stems(normalize(short_desc))
    # Un résumé qui ne serait fait que de mots-outils n'apporte rien non plus.
    if not summary:
        return 1.0

    shared = summary & stems(normalize(description))
    return sum(weight(stem) for stem in shared) / sum(weight(stem) for stem in summary)


@lru_cache(maxsize=10_000)
def merge_description(
    short_desc: str,
    description: str,
    weight: Callable[[str], float] = uniform_weight,
) -> str | None:
    """Description finale d'un couple, ou None si le résumé n'apporte rien.

    Pure, donc mémoïsable : un modèle et ses copies reçoivent le même texte sans recalcul.
    """
    short_desc = short_desc.strip()
    if is_blank(short_desc):
        return None
    if is_blank(description):
        return short_desc

    redundant = (
        bag_coverage(short_desc, description, weight) >= BAG_THRESHOLD
        or sequence_coverage(short_desc, description) >= SEQUENCE_THRESHOLD
    )
    return None if redundant else f"{short_desc}\n\n{description}"


class Command(AtomicHandleMixin, BaseCommand):
    ATOMIC_HANDLE = True
    help = (
        "Réintègre le résumé des services dans leur description : en tête quand il la "
        "complète, abandonné quand il ne fait que la redire."
    )

    def add_arguments(self, parser):
        parser.add_argument("--wet-run", action="store_true")

    @dry_runnable
    def handle(self, *args, **options):
        weight = build_idf(
            Service._base_manager.exclude(description="")
            .values_list("description", flat=True)
            .iterator(chunk_size=BATCH)
        )

        updated, touched_models = [], set()
        copied = dropped = inserted = 0

        services = (
            Service._base_manager.only("pk", "is_model", "short_desc", "description")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for service in services:
            if not service.short_desc.strip():
                continue

            merged = merge_description(service.short_desc, service.description, weight)
            if merged is None:
                dropped += 1
                continue

            if is_blank(service.description):
                copied += 1
            else:
                inserted += 1

            service.description = merged
            if service.is_model:
                touched_models.add(service.pk)
            updated.append(service)
            if len(updated) >= BATCH:
                Service._base_manager.bulk_update(updated, ["description"])
                updated = []

        if updated:
            Service._base_manager.bulk_update(updated, ["description"])

        self.stdout.write(f"{copied:>7} descriptions reprises du résumé")
        self.stdout.write(f"{inserted:>7} résumés insérés en tête de la description")
        self.stdout.write(
            f"{dropped:>7} résumés abandonnés, déjà dits par la description"
        )
        self.stdout.write(
            f"{self._recompute_sync_checksums(touched_models):>7} empreintes recalculées"
        )
        if not options["wet_run"]:
            self.stdout.write(
                self.style.WARNING("Dry-run : aucune modification enregistrée")
            )

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

            # `last_sync_checksum=previous` : seules les copies restées en phase avec leur
            # modèle suivent, celles que leur structure a personnalisées gardent leur écart.
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
