import pytest

from dora.admin_express.models import AdminDivisionType
from dora.decoupage_administratif.models import Commune, Departement, Epci, Region

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
    Commune.objects.create(
        code="75056",
        nom="Paris",
        code_departement="75",
        code_epci="200054781",
        code_region="11",
        codes_postaux=["75001"],
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
    Departement.objects.create(code="75", nom="Paris", code_region="11")

    result = get_diffusion_zone_info(["75"])
    assert result == {
        "diffusion_zone_details": "75",
        "diffusion_zone_details_display": "Paris",
        "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
        "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
    }


@pytest.mark.django_db
def test_get_diffusion_zone_info_department_with_letter():
    Departement.objects.create(code="2A", nom="Corse-du-Sud", code_region="94")

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
    Epci.objects.create(
        code="200054781",
        nom="Métropole du Grand Paris",
        codes_departements=["75", "77", "78", "91", "92", "93", "94", "95"],
        codes_regions=["11"],
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
    Region.objects.create(code="11", nom="Île-de-France")
    Departement.objects.create(code="75", nom="Paris", code_region="11")
    Departement.objects.create(code="77", nom="Seine-et-Marne", code_region="11")
    Departement.objects.create(code="78", nom="Yvelines", code_region="11")
    Departement.objects.create(code="91", nom="Essonne", code_region="11")
    Departement.objects.create(code="92", nom="Hauts-de-Seine", code_region="11")
    Departement.objects.create(code="93", nom="Seine-Saint-Denis", code_region="11")
    Departement.objects.create(code="94", nom="Val-de-Marne", code_region="11")
    Departement.objects.create(code="95", nom="Val-d'Oise", code_region="11")

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
    Region.objects.create(code="11", nom="Île-de-France")
    Departement.objects.create(code="75", nom="Paris", code_region="11")
    Departement.objects.create(code="77", nom="Seine-et-Marne", code_region="11")
    Departement.objects.create(code="78", nom="Yvelines", code_region="11")
    Departement.objects.create(code="91", nom="Essonne", code_region="11")
    Departement.objects.create(code="92", nom="Hauts-de-Seine", code_region="11")
    Departement.objects.create(code="93", nom="Seine-Saint-Denis", code_region="11")
    Departement.objects.create(code="94", nom="Val-de-Marne", code_region="11")
    Departement.objects.create(code="95", nom="Val-d'Oise", code_region="11")

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
    Region.objects.create(code="11", nom="Île-de-France")
    Departement.objects.create(code="75", nom="Paris", code_region="11")
    Departement.objects.create(code="77", nom="Seine-et-Marne", code_region="11")
    Departement.objects.create(code="78", nom="Yvelines", code_region="11")
    Departement.objects.create(code="91", nom="Essonne", code_region="11")
    Departement.objects.create(code="92", nom="Hauts-de-Seine", code_region="11")
    Departement.objects.create(code="93", nom="Seine-Saint-Denis", code_region="11")
    Departement.objects.create(code="94", nom="Val-de-Marne", code_region="11")
    Departement.objects.create(code="95", nom="Val-d'Oise", code_region="11")

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
    Commune.objects.create(
        code="75056",
        nom="Paris",
        code_departement="75",
        code_epci="200054781",
        code_region="11",
        codes_postaux=["75001"],
    )
    Commune.objects.create(
        code="13001",
        nom="Aix-en-Provence",
        code_departement="13",
        code_epci="200054781",
        code_region="93",
        codes_postaux=["13100"],
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
    Commune.objects.create(
        code="75056",
        nom="Paris",
        code_departement="75",
        code_epci="200054781",
        code_region="11",
        codes_postaux=["75001"],
    )
    Commune.objects.create(
        code="13001",
        nom="Aix-en-Provence",
        code_departement="13",
        code_epci="200054781",
        code_region="93",
        codes_postaux=["13100"],
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
    Departement.objects.create(code="971", nom="Guadeloupe", code_region="01")

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
    Region.objects.create(code="94", nom="Corse")
    Departement.objects.create(code="2A", nom="Corse-du-Sud", code_region="94")
    Departement.objects.create(code="2B", nom="Haute-Corse", code_region="94")

    zone_codes = ["2A", "2B"]
    result = get_diffusion_zone_info(zone_codes)
    assert result == {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "Corse",
        "diffusion_zone_type": AdminDivisionType.REGION.value,
        "diffusion_zone_type_display": AdminDivisionType.REGION.label,
    }
