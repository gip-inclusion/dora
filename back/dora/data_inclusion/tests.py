from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice

from .mappings import map_service
from .test_utils import make_di_service_data

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
