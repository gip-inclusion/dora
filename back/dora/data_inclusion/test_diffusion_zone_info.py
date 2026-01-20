import pytest

from dora.admin_express.models import AdminDivisionType
from dora.decoupage_administratif.models import EPCI, City, Department, Region

from .diffusion_zone_info import get_diffusion_zone_info


def test_get_diffusion_zone_info_france():
    assert get_diffusion_zone_info(["france"]) == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "France entière",
        "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
        "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_city():
    City.objects.create(
        code="75056",
        name="Paris",
        department="75",
        epci="200054781",
        region="11",
        postal_codes=["75001"],
    )

    result = get_diffusion_zone_info(["75056"])
    assert result == {
        "diffusion_zone_details": "75056",
        "diffusion_zone_details_display": "Paris (75)",
        "diffusion_zone_type": AdminDivisionType.CITY.value,
        "diffusion_zone_type_display": AdminDivisionType.CITY.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_city_not_found():
    result = get_diffusion_zone_info(["99999"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_department():
    Department.objects.create(code="75", name="Paris", region="11")

    result = get_diffusion_zone_info(["75"])
    assert result == {
        "diffusion_zone_details": "75",
        "diffusion_zone_details_display": "Paris",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_department_with_letter():
    Department.objects.create(code="2A", name="Corse-du-Sud", region="94")

    result = get_diffusion_zone_info(["2A"])
    assert result == {
        "diffusion_zone_details": "2A",
        "diffusion_zone_details_display": "Corse-du-Sud",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_department_not_found():
    result = get_diffusion_zone_info(["99"])
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_epci():
    EPCI.objects.create(
        code="200054781",
        name="Métropole du Grand Paris",
        departments=["75", "77", "78", "91", "92", "93", "94", "95"],
        regions=["11"],
    )

    result = get_diffusion_zone_info(["200054781"])
    assert result == {
        "diffusion_zone_details": "200054781",
        "diffusion_zone_details_display": "Métropole du Grand Paris",
        "diffusion_zone_type": AdminDivisionType.EPCI.value,
        "diffusion_zone_type_display": AdminDivisionType.EPCI.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_epci_not_found():
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


@pytest.mark.django_db
def test_get_diffusion_zone_info_region():
    Region.objects.create(code="11", name="Île-de-France")
    Department.objects.create(code="75", name="Paris", region="11")
    Department.objects.create(code="77", name="Seine-et-Marne", region="11")
    Department.objects.create(code="78", name="Yvelines", region="11")
    Department.objects.create(code="91", name="Essonne", region="11")
    Department.objects.create(code="92", name="Hauts-de-Seine", region="11")
    Department.objects.create(code="93", name="Seine-Saint-Denis", region="11")
    Department.objects.create(code="94", name="Val-de-Marne", region="11")
    Department.objects.create(code="95", name="Val-d'Oise", region="11")

    zone_codes = ["75", "77", "78", "91", "92", "93", "94", "95"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Île-de-France",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_region_different_order():
    Region.objects.create(code="11", name="Île-de-France")
    Department.objects.create(code="75", name="Paris", region="11")
    Department.objects.create(code="77", name="Seine-et-Marne", region="11")
    Department.objects.create(code="78", name="Yvelines", region="11")
    Department.objects.create(code="91", name="Essonne", region="11")
    Department.objects.create(code="92", name="Hauts-de-Seine", region="11")
    Department.objects.create(code="93", name="Seine-Saint-Denis", region="11")
    Department.objects.create(code="94", name="Val-de-Marne", region="11")
    Department.objects.create(code="95", name="Val-d'Oise", region="11")

    zone_codes = ["95", "94", "93", "92", "91", "78", "77", "75"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Île-de-France",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_region_partial():
    Region.objects.create(code="11", name="Île-de-France")
    Department.objects.create(code="75", name="Paris", region="11")
    Department.objects.create(code="77", name="Seine-et-Marne", region="11")
    Department.objects.create(code="78", name="Yvelines", region="11")
    Department.objects.create(code="91", name="Essonne", region="11")
    Department.objects.create(code="92", name="Hauts-de-Seine", region="11")
    Department.objects.create(code="93", name="Seine-Saint-Denis", region="11")
    Department.objects.create(code="94", name="Val-de-Marne", region="11")
    Department.objects.create(code="95", name="Val-d'Oise", region="11")

    zone_codes = ["75", "77"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris, Seine-et-Marne",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_multiple_codes():
    City.objects.create(
        code="75056",
        name="Paris",
        department="75",
        epci="200054781",
        region="11",
        postal_codes=["75001"],
    )
    City.objects.create(
        code="13001",
        name="Aix-en-Provence",
        department="13",
        epci="200054781",
        region="93",
        postal_codes=["13100"],
    )

    zone_codes = ["75056", "13001"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris (75), Aix-en-Provence (13)",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_with_empty_display():
    City.objects.create(
        code="75056",
        name="Paris",
        department="75",
        epci="200054781",
        region="11",
        postal_codes=["75001"],
    )
    City.objects.create(
        code="13001",
        name="Aix-en-Provence",
        department="13",
        epci="200054781",
        region="93",
        postal_codes=["13100"],
    )

    zone_codes = ["75056", "99999", "13001"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Paris (75), Aix-en-Provence (13)",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_all_empty():
    zone_codes = ["99999", "88888"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_guadeloupe():
    Department.objects.create(code="971", name="Guadeloupe", region="01")

    zone_codes = ["971"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": "971",
        "diffusion_zone_details_display": "Guadeloupe",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_corse():
    Region.objects.create(code="94", name="Corse")
    Department.objects.create(code="2A", name="Corse-du-Sud", region="94")
    Department.objects.create(code="2B", name="Haute-Corse", region="94")

    zone_codes = ["2A", "2B"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Corse",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }
