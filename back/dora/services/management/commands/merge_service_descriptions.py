"""Réintégration du résumé des services dans leur description, le temps de la migration.

`Service.short_desc` disparaît au profit d'une description unique, dont les premières lignes
tiendront lieu de résumé. Les deux champs ayant coexisté par dépit, ils ont été employés de
deux façons opposées : certains résumés complètent la description — à conserver, en tête — et
d'autres n'en sont qu'une recopie ou une paraphrase — à jeter.

Ce sont les deux mesures ci-dessous qui tranchent. Aucun texte n'est jamais réécrit : la
description ressort intacte, précédée du résumé, ou remplacée par lui dans le seul cas où
elle ne porte aucun mot. La normalisation ne sert qu'à comparer, jamais à produire, ce qui
met la typographie du texte de référence — espaces insécables et fines, apostrophes courbes,
guillemets français — hors d'atteinte.

`--report` écrit le détail des décisions dans un CSV, les plus incertaines en tête : c'est
la seule prise qu'on ait sur les cas limites tant que `short_desc` existe encore en base.
"""

import csv
import difflib
import math
import re
import unicodedata
from collections import Counter
from typing import Callable, Iterable

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

# Colonnes du rapport : les mesures et le verdict d'abord, les deux textes ensuite — l'ordre
# dans lequel on relit une décision, et non celui dans lequel on la calcule.
REPORT_FIELDNAMES = [
    "marge",
    "verdict",
    "recouvrement_ordonne",
    "recouvrement_desordonne",
    "nb_services",
    "resume",
    "description",
]

# Au-delà de l'un ou l'autre, le résumé n'apporte rien à la description. Deux seuils parce que
# les deux mesures attrapent des redondances de nature différente, cf. plus bas.
SEQUENCE_THRESHOLD = 0.90
BAG_THRESHOLD = 0.90

# Racines tronquées à cette longueur : « accompagnement » et « accompagnons » doivent compter
# pour le même mot, sans embarquer de lemmatiseur.
STEM_LENGTH = 5

# Mots-outils écartés de la comparaison désordonnée : trop fréquents pour distinguer quoi que
# ce soit, ils ne feraient que rapprocher mécaniquement tous les textes. Les mots d'une ou
# deux lettres n'y figurent pas : `stems` les écarte déjà tous.
#
# L'appartenance est testée sur le mot entier, avant troncature, et non sur sa racine : « et
# cetera » y gagnerait quelques formes fléchies — « permettant » passe là où « permet » est
# écarté — mais « entre » emporterait « entreprise », « entretien » et « entreprendre »,
# « comme » emporterait « commerce », et « avant » « avantage ». Le vocabulaire de ce corpus
# ne survit pas à ce raccourci.
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
    """Découpe en mots comparables : casse, accents et ponctuation effacés.

    Volontairement destructeur — c'est ce qui permet de reconnaître « l'Accueil » dans
    « L’accueil ». Le résultat ne sert qu'à mesurer et ne ressort jamais en base.
    """
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(char for char in text if not unicodedata.combining(char))
    return NON_ALPHANUMERIC.sub(" ", APOSTROPHES.sub(" ", text)).split()


def fold(text: str) -> list[str]:
    """Mots comparables d'un texte balisé, le markdown en moins."""
    return normalize(strip_markdown(text))


def is_blank(text: str) -> bool:
    """Le texte se réduit-il à de la ponctuation ou du balisage — « --- », « *** », « ... » ?

    Mesuré sur le texte brut, et non sur `fold` : `strip_markdown` ne voit pas le HTML, dont
    une poignée de descriptions sont entièrement faites. Les prendre pour vides reviendrait
    à jeter le texte de référence, ce que rien n'autorise.
    """
    return not normalize(text)


def stems(words: Iterable[str]) -> set[str]:
    """Racines porteuses de sens d'une suite de mots.

    Les nombres sont retenus quelle que soit leur longueur, là où les mots de moins de trois
    lettres sont écartés : « 16 », « 25 », « 2 » portent l'âge, la durée ou le nombre de
    places — précisément ce qu'un résumé ajoute à une description qui n'en dit rien.
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

    Sans cette pondération, le vocabulaire omniprésent du secteur — « accompagnement »,
    « emploi », « insertion » — suffirait à faire passer pour une paraphrase un résumé qui
    apporte pourtant du neuf.
    """
    document_frequency = Counter()
    total = 0
    for description in descriptions:
        total += 1
        document_frequency.update(stems(fold(description)))

    if not total:
        return uniform_weight

    def weight(stem: str) -> float:
        # `1 + N / (1 + df)` reste strictement positif, y compris pour une racine présente
        # dans toutes les descriptions, là où le `N / (1 + df)` habituel passerait sous zéro
        # et rendrait le ratio de couverture ininterprétable.
        return math.log(1 + total / (1 + document_frequency[stem]))

    return weight


def sequence_coverage(short_desc: str, description: str) -> float:
    """Part du résumé retrouvée *dans l'ordre* dans la description.

    Attrape la recopie et la quasi-recopie — de loin la redondance la plus fréquente — que ni
    une majuscule, ni une incise, ni une coquille ne suffisent à masquer.
    """
    words = fold(short_desc)
    if not words:
        return 1.0

    matcher = difflib.SequenceMatcher(a=words, b=fold(description), autojunk=False)
    matched = sum(block.size for block in matcher.get_matching_blocks())
    return matched / len(words)


def bag_coverage(
    short_desc: str, description: str, weight: Callable[[str], float]
) -> float:
    """Part du résumé retrouvée *sans égard à l'ordre*, pondérée par la rareté des mots.

    Attrape la paraphrase, qui reformule et réordonne mais conserve le vocabulaire propre au
    sujet. La pondération est ce qui distingue « redit la même chose » de « parle du même
    domaine ».
    """
    summary = stems(fold(short_desc))
    if not summary:
        return 1.0

    shared = summary & stems(fold(description))
    total = sum(weight(stem) for stem in summary)
    if not total:
        return len(shared) / len(summary)
    return sum(weight(stem) for stem in shared) / total


def merge_description(
    short_desc: str,
    description: str,
    weight: Callable[[str], float] = uniform_weight,
) -> str | None:
    """Description finale d'un couple, ou None si le résumé n'apporte rien.

    La description est reproduite telle quelle, au caractère près : on ne fait que la précéder
    du résumé, ou la laisser intacte. Elle ne cède la place qu'en ne disant rien du tout.
    """
    short_desc = short_desc.strip()
    # Sans mot, rien à apporter : quelques résumés ne contiennent que du bruit markdown
    # (« --- », « **** »), qui ferait un filet horizontal ou une coquille en tête de fiche.
    if not fold(short_desc):
        return None
    # Le même bruit se rencontre côté description, où il se retrouverait en queue de fiche.
    if is_blank(description):
        return short_desc

    # Le recouvrement désordonné tranche seul près de la moitié des couples, et s'obtient par
    # deux intersections d'ensembles là où l'ordonné aligne deux suites de mots. D'où cet
    # ordre, que la pureté des deux mesures rend indifférent au résultat — l'essentiel du
    # temps se passant de toute façon dans `fold`, il ne fait gagner que quelques pour cent.
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
        parser.add_argument(
            "--report",
            metavar="FICHIER",
            help=(
                "Écrit le détail des décisions dans ce fichier CSV, les plus incertaines en "
                "tête. Produit même en dry-run, et hors transaction : il survit au rollback."
            ),
        )

    @dry_runnable
    def handle(self, *args, **options):
        weight = build_idf(
            Service._base_manager.exclude(description="")
            .values_list("description", flat=True)
            .iterator(chunk_size=BATCH)
        )

        updated, touched_models = [], set()
        # La fusion étant une fonction pure du couple, la mémoriser suffit à garantir qu'un
        # modèle et toutes ses copies reçoivent le même texte — et évite de recalculer les
        # mesures pour chacune.
        merges: dict[tuple[str, str], str | None] = {}
        occurrences: Counter[tuple[str, str]] = Counter()
        copied = dropped = inserted = 0

        # `_base_manager` pour inclure les modèles
        services = (
            Service._base_manager.only("pk", "is_model", "short_desc", "description")
            .order_by("pk")
            .iterator(chunk_size=BATCH)
        )
        for service in services:
            if not service.short_desc.strip():
                continue

            key = (service.short_desc, service.description)
            if key not in merges:
                merges[key] = merge_description(*key, weight)
            merged = merges[key]
            occurrences[key] += 1

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
        if options["report"]:
            written = self._write_report(options["report"], merges, occurrences, weight)
            self.stdout.write(
                f"{written:>7} décisions détaillées dans {options['report']}"
            )
        if not options["wet_run"]:
            self.stdout.write(
                self.style.WARNING("Dry-run : aucune modification enregistrée")
            )

    def _write_report(self, path, merges, occurrences, weight) -> int:
        """Détail des décisions, les plus incertaines en tête.

        La marge dit de combien la mesure la plus haute a dépassé son seuil : négative quand
        le résumé est conservé, positive quand il est abandonné, et d'autant plus proche de
        zéro que la décision s'est jouée à peu de chose. Trier dessus met en tête les seuls
        couples qu'une relecture humaine a intérêt à reprendre.
        """
        rows = []
        for (short_desc, description), merged in merges.items():
            sequence = sequence_coverage(short_desc, description)
            bag = bag_coverage(short_desc, description, weight)
            if merged is None:
                verdict = "abandonné"
            elif is_blank(description):
                verdict = "recopié"
            else:
                verdict = "inséré en tête"
            rows.append(
                {
                    "marge": round(
                        max(sequence - SEQUENCE_THRESHOLD, bag - BAG_THRESHOLD), 3
                    ),
                    "verdict": verdict,
                    "recouvrement_ordonne": round(sequence, 3),
                    "recouvrement_desordonne": round(bag, 3),
                    "nb_services": occurrences[(short_desc, description)],
                    "resume": short_desc,
                    "description": description,
                }
            )

        rows.sort(key=lambda row: abs(row["marge"]))
        # `utf-8-sig` : le rapport se relit dans un tableur, qui sans la marque d'ordre des
        # octets prendrait les accents pour du latin-1.
        with open(path, "w", newline="", encoding="utf-8-sig") as report:
            writer = csv.DictWriter(report, fieldnames=REPORT_FIELDNAMES)
            writer.writeheader()
            writer.writerows(rows)

        return len(rows)

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
