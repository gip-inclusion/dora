import pytest
from django.core.management import call_command
from model_bakery import baker

from dora.core.test_utils import (
    make_model,
    make_service,
    make_structure,
)
from dora.services.descriptions import build_idf, merge_description
from dora.services.models import Service
from dora.services.utils import instantiate_service_from_model, update_sync_checksum

DESCRIPTION = (
    "## Notre offre\n\nNous proposons :\n\n- la **location** de véhicules\n"
    "- un accompagnement au permis\n\nContactez-nous."
)

# La typographie fait partie du texte de l'utilisateur, au même titre que les mots. Écrite
# en échappements : ces caractères sont invisibles à la relecture et un éditeur pourrait les
# normaliser sans qu'on s'en aperçoive, ce qui viderait le test de son objet.
NARROW_NBSP, NBSP, APOSTROPHE = "\u202f", "\u00a0", "\u2019"
TYPOGRAPHY = (
    f"L{APOSTROPHE}accueil{NARROW_NBSP}? Au c\u0153ur du quartier, "
    f"le mardi{NBSP}: «{NBSP}sur rendez-vous{NBSP}»."
)


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "short_desc,description",
    [
        ("Un résumé", "Un résumé"),
        # le résumé est saisi en texte brut, le descriptif en markdown
        ("Un résumé", "**Un résumé** mis en forme"),
        ("Un résumé", "un   RÉSUMÉ\n\nsuivi d'un développement"),
        # recopie à une coquille et une incise près : le cas le plus fréquent en base
        (
            "Nous proposons la location de véhicules et un accompagnement au permis.",
            "Nous proposons, sous conditions, la location de véhicules et un "
            "accompagnement au permis.",
        ),
        # paraphrase : les mots changent et se réordonnent, le sujet non
        (
            "Accompagnement à la création ou au développement d'une entreprise",
            "BGE Picardie est une structure spécialisée dans l'accompagnement à la "
            "création et au développement des entreprises.",
        ),
        ("", DESCRIPTION),
        ("   ", DESCRIPTION),
        # des résumés réduits à du bruit markdown : « --- » ferait un filet horizontal en
        # tête de fiche, et servirait de chapô dans les résultats de recherche
        ("---", DESCRIPTION),
        ("****", ""),
        ("-", ""),
    ],
)
def test_merge_description_drops_a_summary_that_adds_nothing(short_desc, description):
    assert merge_description(short_desc, description) is None


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "short_desc,description",
    [
        ("Un résumé", "Un tout autre descriptif"),
        # un même domaine ne suffit pas : le résumé nomme un service que la description tait
        (
            "Location de scooters et de vélos électriques.",
            "Nos conseillers vous accompagnent dans vos démarches de mobilité.",
        ),
    ],
)
def test_merge_description_keeps_a_summary_that_completes_the_description(
    short_desc, description
):
    assert (
        merge_description(short_desc, description) == f"{short_desc}\n\n{description}"
    )


@pytest.mark.no_django_db
def test_merge_description_copies_the_summary_when_there_is_no_description():
    assert merge_description("Un résumé", "") == "Un résumé"
    assert merge_description("Un résumé", "   \n ") == "Un résumé"


@pytest.mark.no_django_db
def test_merge_description_reproduces_the_description_character_for_character():
    # Le point qui a fait renoncer à une fusion par LLM : la description est le texte de
    # référence, et sa typographie en fait partie.
    merged = merge_description("Permanence numérique le jeudi.", TYPOGRAPHY)

    assert merged is not None
    assert merged.endswith(TYPOGRAPHY)
    assert all(char in merged for char in (NARROW_NBSP, NBSP, APOSTROPHE))


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "short_desc,description",
    [
        # un nombre de deux caractères tient en un mot-outil pour qui compte les lettres :
        # sans lui, le résumé se réduit au vocabulaire de la description et disparaît
        (
            "2 logements meublés à votre disposition",
            "L'association met un logement meublé à disposition.",
        ),
        (
            "Accompagnement des jeunes de 16 à 25 ans",
            "Nous accompagnons les jeunes dans leur parcours.",
        ),
    ],
)
def test_merge_description_counts_the_numbers_a_summary_adds(short_desc, description):
    assert merge_description(short_desc, description) is not None


@pytest.mark.no_django_db
def test_merge_description_replaces_a_description_reduced_to_markup():
    # le pendant du résumé sans mot : « --- » ferait un filet horizontal en queue de fiche
    assert merge_description("Un résumé", "---") == "Un résumé"
    assert merge_description("Un résumé", "  ***  ") == "Un résumé"


@pytest.mark.no_django_db
def test_merge_description_accepts_a_result_beyond_the_field_length():
    # `max_length` ne vaut que pour les formulaires : mieux vaut une description trop longue
    # qu'un résumé perdu.
    description = "Un développement singulier. " * 400
    merged = merge_description("Ouvert à tous, sans rendez-vous.", description)

    assert len(merged) > 10_000
    assert merged.endswith(description)


@pytest.mark.no_django_db
def test_idf_weighting_separates_a_shared_topic_from_a_repeated_one():
    # Le vocabulaire du secteur est partout : sans pondération, il rapprocherait n'importe
    # quels deux textes du champ de l'insertion.
    corpus = [
        "Accompagnement vers l'emploi et l'insertion professionnelle."
        for _ in range(50)
    ] + ["Location de scooters à tarif solidaire."]
    weight = build_idf(corpus)

    assert weight("locat") > weight("emplo")


@pytest.mark.no_django_db
def test_idf_saves_a_summary_whose_only_addition_is_a_rare_name():
    # Cas relevé en base : le résumé ne se distingue que par le sigle de la structure, que
    # la description ne reprend pas. Sous pondération neutre il pèse autant qu'« insertion »
    # et le résumé passe pour une paraphrase ; l'IDF lui rend son poids.
    short_desc = (
        "PROTIS - PROGRAMME ORIENTATION INSERTION SOCIALE propose des services : "
        "réaliser des démarches administratives avec un accompagnement"
    )
    description = (
        "Programme d'Insertion et d'Orientation Sociale propose des services : numérique, "
        "réaliser des démarches administratives avec un accompagnement."
    )
    weight = build_idf(
        [
            f"Structure numéro {n} : programme d'insertion et d'orientation sociale, "
            "propose des services de réalisation de démarches administratives avec un "
            "accompagnement."
            for n in range(40)
        ]
    )

    assert merge_description(short_desc, description) is None
    assert merge_description(short_desc, description, weight) is not None


def empty_the_description(service):
    """Remet le service dans l'état où le déploiement le trouve : description à composer."""
    Service._base_manager.filter(pk=service.pk).update(description="")


@pytest.mark.parametrize(
    "short_desc,full_desc,expected",
    [
        (
            "Un résumé",
            "Un tout autre descriptif",
            "Un résumé\n\nUn tout autre descriptif",
        ),
        ("Un résumé", "**Un résumé** mis en forme", "**Un résumé** mis en forme"),
        ("Un résumé", "", "Un résumé"),
    ],
)
def test_description_is_derived_from_the_pair(short_desc, full_desc, expected):
    service = make_service(short_desc=short_desc, full_desc=full_desc)

    assert service.description == expected


def test_partial_save_leaves_the_description_alone():
    # L'instance vient souvent d'un `only()` qui n'a chargé ni résumé ni descriptif.
    service = make_service(short_desc="Un résumé", full_desc="Un descriptif")
    empty_the_description(service)

    service = Service._base_manager.get(pk=service.pk)
    service.name = "Un autre nom"
    service.save(update_fields=["name"])

    service.refresh_from_db()
    assert service.description == ""


def test_sync_checksum_ignores_the_derived_description():
    # Ce qui dispense d'une migration de recalcul des empreintes.
    model = make_model(short_desc="Un résumé", full_desc="Un descriptif")
    checksum = update_sync_checksum(model)

    model.description = "Une description composée autrement"

    assert update_sync_checksum(model) == checksum


def test_merge_copies_short_desc_when_full_desc_is_empty():
    service = make_service(short_desc="Un résumé", full_desc="")
    modification_date = service.modification_date

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.full_desc == "Un résumé"
    # la date de modification pilote les rappels « service à actualiser »
    assert service.modification_date == modification_date


def test_merge_dry_run_writes_nothing():
    service = make_service(short_desc="Un résumé", full_desc="")

    call_command("merge_service_descriptions")

    service.refresh_from_db()
    assert service.full_desc == ""


def test_merge_inserts_the_summary_ahead_of_the_full_desc():
    service = make_service(short_desc="Un résumé", full_desc="Un tout autre descriptif")

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.full_desc == "Un résumé\n\nUn tout autre descriptif"


def test_merge_leaves_a_full_desc_that_already_says_it():
    service = make_service(
        short_desc="Un résumé", full_desc="**Un résumé** mis en forme"
    )

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.full_desc == "**Un résumé** mis en forme"


def test_merge_keeps_copies_in_sync():
    structure = make_structure(baker.make("users.User", is_valid=True))
    model = make_model(
        structure=structure,
        short_desc="Un résumé",
        full_desc="Un tout autre descriptif",
    )
    synced = instantiate_service_from_model(model, structure, structure.creator)
    customized = instantiate_service_from_model(model, structure, structure.creator)
    Service._base_manager.filter(pk=customized.pk).update(last_sync_checksum="périmé")

    call_command("merge_service_descriptions", "--wet-run")

    model.refresh_from_db()
    synced.refresh_from_db()
    customized.refresh_from_db()
    # même fusion pour le modèle et ses copies : aucune ne doit passer en « modifié »…
    assert (
        synced.full_desc == model.full_desc == "Un résumé\n\nUn tout autre descriptif"
    )
    assert model.sync_checksum == update_sync_checksum(model)
    assert synced.last_sync_checksum == model.sync_checksum
    # … et celles qui l'étaient déjà le restent
    assert customized.last_sync_checksum == "périmé"
