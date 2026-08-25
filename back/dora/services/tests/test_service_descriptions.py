import pytest
from django.core.management import call_command
from model_bakery import baker

from dora.core.test_utils import (
    make_model,
    make_published_service,
    make_service,
    make_structure,
)
from dora.services.management.commands.merge_service_descriptions import (
    build_idf,
    merge_description,
)
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


def test_service_exposes_description_and_its_alias(api_client):
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    assert api_client.get(f"/services/{service.slug}/").data["full_desc"] == "Avant"

    response = api_client.patch(f"/services/{service.slug}/", {"full_desc": "Après"})

    assert response.status_code == 200
    service.refresh_from_db()
    assert service.description == "Après"


def test_alias_takes_precedence_over_description(api_client):
    # Ce que poste un front non basculé : il édite `full_desc` et réexpédie tel quel le
    # `description` reçu au chargement. Retenir ce dernier annulerait la modification.
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    api_client.patch(
        f"/services/{service.slug}/",
        {"full_desc": "Après", "description": "Avant"},
    )

    service.refresh_from_db()
    assert service.description == "Après"


def test_merge_copies_short_desc_when_description_is_empty():
    service = make_service(short_desc="Un résumé", description="")
    modification_date = service.modification_date

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.description == "Un résumé"
    # la date de modification pilote les rappels « service à actualiser »
    assert service.modification_date == modification_date


def test_merge_dry_run_writes_nothing():
    service = make_service(short_desc="Un résumé", description="")

    call_command("merge_service_descriptions")

    service.refresh_from_db()
    assert service.description == ""


def test_merge_inserts_the_summary_ahead_of_the_description():
    service = make_service(
        short_desc="Un résumé", description="Un tout autre descriptif"
    )

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.description == "Un résumé\n\nUn tout autre descriptif"


def test_merge_leaves_a_description_that_already_says_it():
    service = make_service(
        short_desc="Un résumé", description="**Un résumé** mis en forme"
    )

    call_command("merge_service_descriptions", "--wet-run")

    service.refresh_from_db()
    assert service.description == "**Un résumé** mis en forme"


def test_merge_keeps_copies_in_sync():
    structure = make_structure(baker.make("users.User", is_valid=True))
    model = make_model(
        structure=structure,
        short_desc="Un résumé",
        description="Un tout autre descriptif",
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
        synced.description
        == model.description
        == "Un résumé\n\nUn tout autre descriptif"
    )
    assert model.sync_checksum == update_sync_checksum(model)
    assert synced.last_sync_checksum == model.sync_checksum
    # … et celles qui l'étaient déjà le restent
    assert customized.last_sync_checksum == "périmé"
