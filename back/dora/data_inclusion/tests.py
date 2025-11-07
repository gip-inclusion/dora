import pytest
from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice

from .constants import THEMATIQUES_MAPPING_DI_TO_DORA
from .mappings import map_service
from .test_utils import FakeDataInclusionClient, make_di_service_data

ALL_DI_ORIENTATION_MODES = [
    ModeMobilisation.ENVOYER_UN_COURRIEL,
    ModeMobilisation.SE_PRESENTER,
    ModeMobilisation.TELEPHONER,
    ModeMobilisation.UTILISER_LIEN_MOBILISATION,
]

ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES = [
    "envoyer-un-mail",
    "telephoner",
    "completer-le-formulaire-dadhesion",
    "formulaire-dora",
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
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation="https://example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "formulaire-dora",
            ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_with_form_mode_but_no_form_with_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation=None,
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion",
            ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_with_form_mode_but_no_form_without_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=ALL_DI_ORIENTATION_MODES,
        lien_mobilisation=None,
        courriel=None,
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion"
            and m != "formulaire-dora",
            ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_without_form_mode_with_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=list(
            filter(
                lambda m: m != ModeMobilisation.UTILISER_LIEN_MOBILISATION,
                ALL_DI_ORIENTATION_MODES,
            )
        ),
        courriel="contact@example.com",
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion",
            ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES,
        )
    )

    assert sorted(service["coach_orientation_modes"]) == sorted(
        expected_dora_coach_orientation_modes
    )


def test_map_service_coach_orientation_modes_mapping_without_form_mode_without_email():
    di_service_data = make_di_service_data(
        mobilisable_par=[PersonneMobilisatrice.PROFESSIONNELS],
        modes_mobilisation=list(
            filter(
                lambda m: m != ModeMobilisation.UTILISER_LIEN_MOBILISATION,
                ALL_DI_ORIENTATION_MODES,
            )
        ),
        courriel=None,
    )
    service = map_service(di_service_data, False)

    expected_dora_coach_orientation_modes = list(
        filter(
            lambda m: m != "completer-le-formulaire-dadhesion"
            and m != "formulaire-dora",
            ALL_EXPECTED_MAPPED_DORA_COACH_ORIENTATION_MODES,
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
