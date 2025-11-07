from unittest.mock import Mock, patch

from data_inclusion.schema.v1 import ModeMobilisation, PersonneMobilisatrice

from .mappings import map_service
from .test_utils import make_di_service_data
from .zone_codes import get_zone_code_display, get_zone_codes_display

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


def test_get_zone_code_display_france():
    assert get_zone_code_display("france") == "France entière"


@patch("dora.data_inclusion.zone_codes.City.objects.get_from_code")
def test_get_zone_code_display_city(mock_get_city):
    mock_city = Mock()
    mock_city.name = "Paris"
    mock_city.department = "75"
    mock_get_city.return_value = mock_city

    result = get_zone_code_display("75056")
    assert result == "Paris (75)"


@patch("dora.data_inclusion.zone_codes.City.objects.get_from_code")
def test_get_zone_code_display_city_not_found(mock_get_city):
    mock_get_city.return_value = None

    result = get_zone_code_display("99999")
    assert result == ""


@patch("dora.data_inclusion.zone_codes.Department.objects.get_from_code")
def test_get_zone_code_display_department(mock_get_department):
    mock_department = Mock()
    mock_department.name = "Paris"
    mock_get_department.return_value = mock_department

    result = get_zone_code_display("75")
    assert result == "Paris"


@patch("dora.data_inclusion.zone_codes.Department.objects.get_from_code")
def test_get_zone_code_display_department_with_letter(mock_get_department):
    mock_department = Mock()
    mock_department.name = "Corse-du-Sud"
    mock_get_department.return_value = mock_department

    result = get_zone_code_display("2A")
    assert result == "Corse-du-Sud"


@patch("dora.data_inclusion.zone_codes.Department.objects.get_from_code")
def test_get_zone_code_display_department_not_found(mock_get_department):
    mock_get_department.return_value = None

    result = get_zone_code_display("99")
    assert result == ""


@patch("dora.data_inclusion.zone_codes.EPCI.objects.get_from_code")
def test_get_zone_code_display_epci(mock_get_epci):
    mock_epci = Mock()
    mock_epci.name = "Métropole du Grand Paris"
    mock_get_epci.return_value = mock_epci

    result = get_zone_code_display("200054781")
    assert result == "Métropole du Grand Paris"


@patch("dora.data_inclusion.zone_codes.EPCI.objects.get_from_code")
def test_get_zone_code_display_epci_not_found(mock_get_epci):
    mock_get_epci.return_value = None

    result = get_zone_code_display("999999999")
    assert result == ""


def test_get_zone_code_display_country_france():
    result = get_zone_code_display("99100")
    assert result == "France entière"


def test_get_zone_code_display_country_other():
    result = get_zone_code_display("99001")
    assert result == ""


def test_get_zone_code_display_unknown():
    result = get_zone_code_display("unknown")
    assert result == ""


def test_get_zone_codes_display_region():
    zone_codes = ["75", "77", "78", "91", "92", "93", "94", "95"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Île-de-France"


def test_get_zone_codes_display_region_different_order():
    zone_codes = ["95", "94", "93", "92", "91", "78", "77", "75"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Île-de-France"


@patch("dora.data_inclusion.zone_codes.Department.objects.get_from_code")
def test_get_zone_codes_display_region_partial(mock_get_department):
    mock_dept_75 = Mock()
    mock_dept_75.name = "Paris"
    mock_dept_77 = Mock()
    mock_dept_77.name = "Seine-et-Marne"
    mock_get_department.side_effect = lambda code: {
        "75": mock_dept_75,
        "77": mock_dept_77,
    }.get(code)

    zone_codes = ["75", "77"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Paris, Seine-et-Marne"


@patch("dora.data_inclusion.zone_codes.City.objects.get_from_code")
def test_get_zone_codes_display_multiple_codes(mock_get_city):
    mock_city_75056 = Mock()
    mock_city_75056.name = "Paris"
    mock_city_75056.department = "75"
    mock_city_13001 = Mock()
    mock_city_13001.name = "Aix-en-Provence"
    mock_city_13001.department = "13"
    mock_get_city.side_effect = lambda code: {
        "75056": mock_city_75056,
        "13001": mock_city_13001,
    }.get(code)

    zone_codes = ["75056", "13001"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Paris (75), Aix-en-Provence (13)"


@patch("dora.data_inclusion.zone_codes.City.objects.get_from_code")
def test_get_zone_codes_display_with_empty_display(mock_get_city):
    mock_city_75056 = Mock()
    mock_city_75056.name = "Paris"
    mock_city_75056.department = "75"
    mock_city_13001 = Mock()
    mock_city_13001.name = "Aix-en-Provence"
    mock_city_13001.department = "13"
    mock_get_city.side_effect = lambda code: {
        "75056": mock_city_75056,
        "13001": mock_city_13001,
        "99999": None,
    }.get(code)

    zone_codes = ["75056", "99999", "13001"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Paris (75), Aix-en-Provence (13)"


@patch("dora.data_inclusion.zone_codes.City.objects.get_from_code")
def test_get_zone_codes_display_all_empty(mock_get_city):
    mock_get_city.return_value = None

    zone_codes = ["99999", "88888"]
    result = get_zone_codes_display(zone_codes)
    assert result == ""


def test_get_zone_codes_display_guadeloupe():
    zone_codes = ["971"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Guadeloupe"


def test_get_zone_codes_display_corse():
    zone_codes = ["2A", "2B"]
    result = get_zone_codes_display(zone_codes)
    assert result == "Corse"
