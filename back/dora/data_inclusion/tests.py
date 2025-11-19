from .mappings import map_service
from .test_utils import make_di_service_data

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
