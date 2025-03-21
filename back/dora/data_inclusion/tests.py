import pytest

from .constants import THEMATIQUES_MAPPING_DI_TO_DORA
from .mappings import map_service
from .test_utils import FakeDataInclusionClient, make_di_service_data

ALL_DI_COACH_ORIENTATION_MODES = [
    "autre",
    "completer-le-formulaire-dadhesion",
    "envoyer-un-mail",
    "envoyer-un-mail-avec-une-fiche-de-prescription",
    "telephoner",
    "prendre-rdv",
]

ALL_DORA_COACH_ORIENTATION_MODES = [
    "autre",
    "completer-le-formulaire-dadhesion",
    "envoyer-un-mail",
    "envoyer-un-mail-avec-une-fiche-de-prescription",
    "formulaire-dora",
    "telephoner",
]


def test_map_service_thematiques_mapping():
    input_thematiques = [
        "logement-hebergement",
        "logement-hebergement--connaissance-de-ses-droits-et-interlocuteurs",
        "logement-hebergement--besoin-dadapter-mon-logement",
    ] + list(THEMATIQUES_MAPPING_DI_TO_DORA.keys())

    expected_categories = ["logement-hebergement"]
    expected_subcategories = [
        "logement-hebergement--connaissance-de-ses-droits-et-interlocuteurs",
        "logement-hebergement--besoin-dadapter-mon-logement",
    ] + list(THEMATIQUES_MAPPING_DI_TO_DORA.values())

    di_service_data = make_di_service_data(thematiques=input_thematiques)
    service = map_service(di_service_data, False)

    assert sorted(service["categories"]) == sorted(expected_categories)
    assert sorted(service["subcategories"]) == sorted(expected_subcategories)


@pytest.mark.parametrize(
    "thematiques_dora, thematiques_di",
    [
        (
            ["logement-hebergement--etre-accompagne-pour-se-loger"],
            ["logement-hebergement--etre-accompagne-dans-son-projet-accession"],
        ),
        (
            ["logement-hebergement--gerer-son-budget"],
            ["logement-hebergement--etre-accompagne-en cas-de-difficultes-financieres"],
        ),
        (
            ["logement-hebergement--autre"],
            ["logement-hebergement--financer-son-projet-travaux"],
        ),
    ],
)
def test_di_client_search_thematiques_mapping(thematiques_dora, thematiques_di):
    di_client = FakeDataInclusionClient()
    di_service_data = make_di_service_data(thematiques=thematiques_di)
    di_client.services.append(di_service_data)

    results = di_client.search_services(thematiques=thematiques_dora)

    assert len(results) == 1


def test_map_service_coach_orientation_modes_mapping_with_form_mode_and_form():
    di_service_data = make_di_service_data(
        modes_orientation_accompagnateur=ALL_DI_COACH_ORIENTATION_MODES,
        formulaire_en_ligne="https://example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "formulaire-dora",
            ALL_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_with_form_mode_but_no_form_with_email():
    di_service_data = make_di_service_data(
        modes_orientation_accompagnateur=ALL_DI_COACH_ORIENTATION_MODES,
        formulaire_en_ligne=None,
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion",
            ALL_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_with_form_mode_but_no_form_without_email():
    di_service_data = make_di_service_data(
        modes_orientation_accompagnateur=ALL_DI_COACH_ORIENTATION_MODES,
        formulaire_en_ligne=None,
        courriel=None,
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion"
            and m != "formulaire-dora",
            ALL_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_without_form_mode_with_email():
    di_service_data = make_di_service_data(
        modes_orientation_accompagnateur=list(
            filter(
                lambda m: m != "completer-le-formulaire-dadhesion",
                ALL_DI_COACH_ORIENTATION_MODES,
            )
        ),
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion",
            ALL_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_without_form_mode_without_email():
    di_service_data = make_di_service_data(
        modes_orientation_accompagnateur=list(
            filter(
                lambda m: m != "completer-le-formulaire-dadhesion",
                ALL_DI_COACH_ORIENTATION_MODES,
            )
        ),
        courriel=None,
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion"
            and m != "formulaire-dora",
            ALL_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_address_line():
    di_service_data = make_di_service_data(
        adresse="6 Boulevard St Denis",
        complement_adresse="Plateforme de l'inclusion",
        code_postal="75010",
        commune="Paris",
    )
    service = map_service(di_service_data, False)

    assert (
        service["address_line"]
        == "6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris"
    )
