from unittest.mock import Mock, patch

from dora.admin_express.models import AdminDivisionType

from .diffusion_zone_info import get_diffusion_zone_info


def test_get_diffusion_zone_info_france():
    assert get_diffusion_zone_info(["france"]) == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "France entière",
        "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
        "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
    }


@patch("dora.admin_express.models.City.objects.get_from_code")
def test_get_diffusion_zone_info_city(mock_get_city):
    mock_city = Mock()
    mock_city.code = "75056"
    mock_city.name = "Paris"
    mock_city.department = "75"
    mock_get_city.return_value = mock_city

    result = get_diffusion_zone_info(["75056"])
    assert result == {
        "diffusion_zone_details": "75056",
        "diffusion_zone_details_display": "Paris (75)",
        "diffusion_zone_type": AdminDivisionType.CITY.value,
        "diffusion_zone_type_display": AdminDivisionType.CITY.label,
    }


@patch("dora.admin_express.models.City.objects.get_from_code")
def test_get_diffusion_zone_info_city_not_found(mock_get_city):
    mock_get_city.return_value = None

    result = get_diffusion_zone_info(["99999"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@patch("dora.admin_express.models.Department.objects.get_from_code")
def test_get_diffusion_zone_info_department(mock_get_department):
    mock_department = Mock()
    mock_department.code = "75"
    mock_department.name = "Paris"
    mock_get_department.return_value = mock_department

    result = get_diffusion_zone_info(["75"])
    assert result == {
        "diffusion_zone_details": "75",
        "diffusion_zone_details_display": "Paris",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@patch("dora.admin_express.models.Department.objects.get_from_code")
def test_get_diffusion_zone_info_department_with_letter(mock_get_department):
    mock_department = Mock()
    mock_department.code = "2A"
    mock_department.name = "Corse-du-Sud"
    mock_get_department.return_value = mock_department

    result = get_diffusion_zone_info(["2A"])
    assert result == {
        "diffusion_zone_details": "2A",
        "diffusion_zone_details_display": "Corse-du-Sud",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@patch("dora.admin_express.models.Department.objects.get_from_code")
def test_get_diffusion_zone_info_department_not_found(mock_get_department):
    mock_get_department.return_value = None

    result = get_diffusion_zone_info(["99"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@patch("dora.admin_express.models.EPCI.objects.get_from_code")
def test_get_diffusion_zone_info_epci(mock_get_epci):
    mock_epci = Mock()
    mock_epci.code = "200054781"
    mock_epci.name = "Métropole du Grand Paris"
    mock_get_epci.return_value = mock_epci

    result = get_diffusion_zone_info(["200054781"])
    assert result == {
        "diffusion_zone_details": "200054781",
        "diffusion_zone_details_display": "Métropole du Grand Paris",
        "diffusion_zone_type": AdminDivisionType.EPCI.value,
        "diffusion_zone_type_display": AdminDivisionType.EPCI.label,
    }


@patch("dora.admin_express.models.EPCI.objects.get_from_code")
def test_get_diffusion_zone_info_epci_not_found(mock_get_epci):
    mock_get_epci.return_value = None

    result = get_diffusion_zone_info(["999999999"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


def test_get_diffusion_zone_info_country_france():
    result = get_diffusion_zone_info(["99100"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "France entière",
        "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
        "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
    }


def test_get_diffusion_zone_info_country_other():
    result = get_diffusion_zone_info(["99001"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


def test_get_diffusion_zone_info_unknown():
    result = get_diffusion_zone_info(["unknown"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


def test_get_diffusion_zone_info_region():
    zone_codes = ["75", "77", "78", "91", "92", "93", "94", "95"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Île-de-France",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }


def test_get_diffusion_zone_info_region_different_order():
    zone_codes = ["95", "94", "93", "92", "91", "78", "77", "75"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Île-de-France",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }


@patch("dora.admin_express.models.Department.objects.get_from_code")
def test_get_diffusion_zone_info_region_partial(mock_get_department):
    mock_dept_75 = Mock()
    mock_dept_75.code = "75"
    mock_dept_75.name = "Paris"
    mock_dept_77 = Mock()
    mock_dept_77.code = "77"
    mock_dept_77.name = "Seine-et-Marne"
    mock_get_department.side_effect = lambda code: {
        "75": mock_dept_75,
        "77": mock_dept_77,
    }.get(code)

    zone_codes = ["75", "77"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris, Seine-et-Marne",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@patch("dora.admin_express.models.City.objects.get_from_code")
def test_get_diffusion_zone_info_multiple_codes(mock_get_city):
    mock_city_75056 = Mock()
    mock_city_75056.code = "75056"
    mock_city_75056.name = "Paris"
    mock_city_75056.department = "75"
    mock_city_13001 = Mock()
    mock_city_13001.code = "13001"
    mock_city_13001.name = "Aix-en-Provence"
    mock_city_13001.department = "13"
    mock_get_city.side_effect = lambda code: {
        "75056": mock_city_75056,
        "13001": mock_city_13001,
    }.get(code)

    zone_codes = ["75056", "13001"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris (75), Aix-en-Provence (13)",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@patch("dora.admin_express.models.City.objects.get_from_code")
def test_get_diffusion_zone_info_with_empty_display(mock_get_city):
    mock_city_75056 = Mock()
    mock_city_75056.code = "75056"
    mock_city_75056.name = "Paris"
    mock_city_75056.department = "75"
    mock_city_13001 = Mock()
    mock_city_13001.code = "13001"
    mock_city_13001.name = "Aix-en-Provence"
    mock_city_13001.department = "13"
    mock_get_city.side_effect = lambda code: {
        "75056": mock_city_75056,
        "13001": mock_city_13001,
        "99999": None,
    }.get(code)

    zone_codes = ["75056", "99999", "13001"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris (75), Aix-en-Provence (13)",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@patch("dora.admin_express.models.City.objects.get_from_code")
def test_get_diffusion_zone_info_all_empty(mock_get_city):
    mock_get_city.return_value = None

    zone_codes = ["99999", "88888"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


def test_get_diffusion_zone_info_guadeloupe():
    zone_codes = ["971"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Guadeloupe",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }


def test_get_diffusion_zone_info_corse():
    zone_codes = ["2A", "2B"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Corse",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }
