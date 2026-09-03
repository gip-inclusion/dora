"""Composition de la description d'un service à partir de son résumé et de son descriptif.

Le résumé est repris en tête quand il complète le descriptif, abandonné quand il ne fait que
le redire. Aucun texte n'est jamais réécrit : `normalize` ne sert qu'à comparer, jamais à
produire, ce qui met la typographie du texte de référence hors d'atteinte.
"""

import difflib
import math
import re
import unicodedata
from collections import Counter
from functools import lru_cache
from typing import Callable, Iterable

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
    souvent tout ce qu'un résumé ajoute à un descriptif qui n'en dit rien.
    """
    return {
        word[:STEM_LENGTH]
        for word in words
        if (word.isdigit() or len(word) > 2) and word not in STOPWORDS
    }


def uniform_weight(stem: str) -> float:
    """Pondération neutre, quand aucun corpus n'est disponible pour en tirer une."""
    return 1.0


def build_idf(corpus: Iterable[str]) -> Callable[[str], float]:
    """Poids de rareté d'une racine, tiré du corpus des descriptifs.

    Sans elle, le vocabulaire omniprésent du secteur — « accompagnement », « insertion » —
    ferait passer pour une paraphrase un résumé qui apporte du neuf.
    """
    document_frequency = Counter()
    total = 0
    for text in corpus:
        total += 1
        document_frequency.update(stems(normalize(text)))

    if not total:
        return uniform_weight

    def weight(stem: str) -> float:
        # `1 + N / (1 + df)` reste strictement positif même pour une racine présente partout,
        # là où le `N / (1 + df)` habituel passerait sous zéro.
        return math.log(1 + total / (1 + document_frequency[stem]))

    return weight


def sequence_coverage(short_desc: str, full_desc: str) -> float:
    """Part du résumé retrouvée *dans l'ordre* dans le descriptif : la recopie."""
    words = normalize(short_desc)
    matcher = difflib.SequenceMatcher(a=words, b=normalize(full_desc), autojunk=False)
    # Les blocs d'un seul mot ne sont que des mots-outils tombés au bon endroit : dans un
    # descriptif long, ils suffiraient à faire passer n'importe quel résumé pour une recopie.
    matched = sum(
        block.size for block in matcher.get_matching_blocks() if block.size >= 2
    )
    return matched / len(words)


def bag_coverage(
    short_desc: str, full_desc: str, weight: Callable[[str], float]
) -> float:
    """Part du résumé retrouvée *sans égard à l'ordre*, pondérée par la rareté : la paraphrase."""
    summary = stems(normalize(short_desc))
    # Un résumé qui ne serait fait que de mots-outils n'apporte rien non plus.
    if not summary:
        return 1.0

    shared = summary & stems(normalize(full_desc))
    return sum(weight(stem) for stem in shared) / sum(weight(stem) for stem in summary)


@lru_cache(maxsize=10_000)
def merge_description(
    short_desc: str,
    full_desc: str,
    weight: Callable[[str], float] = uniform_weight,
) -> str | None:
    """Description d'un couple, ou None si le résumé n'apporte rien au descriptif.

    Pure, donc mémoïsable : un modèle et ses copies reçoivent le même texte sans recalcul.
    """
    short_desc = short_desc.strip()
    if is_blank(short_desc):
        return None
    if is_blank(full_desc):
        return short_desc

    redundant = (
        bag_coverage(short_desc, full_desc, weight) >= BAG_THRESHOLD
        or sequence_coverage(short_desc, full_desc) >= SEQUENCE_THRESHOLD
    )
    return None if redundant else f"{short_desc}\n\n{full_desc}"


def merged_description(
    short_desc: str,
    full_desc: str,
    weight: Callable[[str], float] = uniform_weight,
) -> str:
    """Description dérivée d'un couple, toujours un texte.

    Là où `merge_description` distingue le résumé sans apport — `None` — de celui qu'il faut
    reprendre, la description dérivée d'un service n'a que faire de la nuance : sans apport,
    elle vaut le descriptif.
    """
    return merge_description(short_desc, full_desc, weight) or full_desc


def derive_description(
    short_desc: str,
    full_desc: str,
    weight: Callable[[str], float] = uniform_weight,
) -> tuple[str, str | None]:
    """Description dérivée et motif de composition pour le backfill."""
    merged = merge_description(short_desc, full_desc, weight)
    if merged is None:
        if not is_blank(short_desc):
            return full_desc, "dropped"
        return full_desc, None
    if is_blank(full_desc):
        return merged, "copied"
    return merged, "composed"


def backfill_service_descriptions(*, batch: int = 500) -> dict[str, int]:
    from dora.services.models import Service

    weight = build_idf(
        Service._base_manager.exclude(full_desc="")
        .values_list("full_desc", flat=True)
        .iterator(chunk_size=batch)
    )

    stats = {"composed": 0, "copied": 0, "dropped": 0, "written": 0}
    updated = []

    services = (
        Service._base_manager.only("pk", "short_desc", "full_desc", "description")
        .order_by("pk")
        .iterator(chunk_size=batch)
    )
    for service in services:
        description, reason = derive_description(
            service.short_desc, service.full_desc, weight
        )
        if reason:
            stats[reason] += 1
        if description == service.description:
            continue

        service.description = description
        stats["written"] += 1
        updated.append(service)
        if len(updated) >= batch:
            Service._base_manager.bulk_update(updated, ["description"])
            updated = []

    if updated:
        Service._base_manager.bulk_update(updated, ["description"])

    return stats
