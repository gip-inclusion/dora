import re

from dora.admin_express.models import AdminDivisionType
from dora.decoupage_administratif.models import EPCI, City, Department, Region

FRANCE_INSEE_CODE = "99100"

COUNTRY_CODE_PATTERN = r"^99[0-5]\d{2}$"
CITY_CODE_PATTERN = r"^\w{5}$"
DEPARTMENT_CODE_PATTERN = r"^\w{2,3}$"
EPCI_CODE_PATTERN = r"^\d{9}$"
REGION_CODE_PATTERN = r"^\w{2}$"


def get_diffusion_zone_info_for_zone_code(zone_code: str) -> dict:
    if zone_code in ["france", FRANCE_INSEE_CODE]:
        return {
            "diffusion_zone_details": None,
            "diffusion_zone_details_display": "France entière",
            "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
            "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
        }

    if re.match(CITY_CODE_PATTERN, zone_code):
        city = City.objects.filter(code=zone_code).first()
        if city:
            return {
                "diffusion_zone_details": city.code,
                "diffusion_zone_details_display": f"{city.name} ({city.department})",
                "diffusion_zone_type": AdminDivisionType.CITY.value,
                "diffusion_zone_type_display": AdminDivisionType.CITY.label,
            }

    if re.match(DEPARTMENT_CODE_PATTERN, zone_code):
        department = Department.objects.filter(code=zone_code).first()
        if department:
            return {
                "diffusion_zone_details": department.code,
                "diffusion_zone_details_display": department.name,
                "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
                "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
            }

    if re.match(EPCI_CODE_PATTERN, zone_code):
        epci = EPCI.objects.filter(code=zone_code).first()
        if epci:
            return {
                "diffusion_zone_details": epci.code,
                "diffusion_zone_details_display": epci.name,
                "diffusion_zone_type": AdminDivisionType.EPCI.value,
                "diffusion_zone_type_display": AdminDivisionType.EPCI.label,
            }

    return {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": "",
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }


def are_department_codes(department_codes: set[str]) -> bool:
    # Codes attendus : 2 ou 3 lettres ou chiffres
    return all(re.match(DEPARTMENT_CODE_PATTERN, code) for code in department_codes)


def get_region_if_all_department_codes_belong_to_it(
    department_codes: list[str],
) -> Region | None:
    department_codes = set(department_codes)

    if not department_codes:
        # Liste vide
        return None

    if not are_department_codes(department_codes):
        # Un ou plusieurs codes n'ont pas le format attendu
        return None

    departments = list(
        Department.objects.filter(code__in=department_codes).values("code", "region")
    )

    if len(departments) != len(department_codes):
        # Un ou plusieurs codes ne correspondent pas à des départements
        return None

    region_codes = {dept["region"] for dept in departments}

    if len(region_codes) != 1:
        # Les départements ne correspondent pas à une seule région
        return None

    region_code = region_codes.pop()
    region_departments_count = Department.objects.filter(region=region_code).count()

    if region_departments_count != len(department_codes):
        # La région comporte un nombre de départements différent des départements fournis
        return None

    # Tous les départements correspondent à une seule région
    return Region.objects.filter(code=region_code).first()


def get_diffusion_zone_info(zone_codes: list[str] | None) -> list[str]:
    if zone_codes is None:
        return {
            "diffusion_zone_details": None,
            "diffusion_zone_details_display": "",
            "diffusion_zone_type": None,
            "diffusion_zone_type_display": "",
        }

    if len(zone_codes) == 1:
        return get_diffusion_zone_info_for_zone_code(zone_codes[0])

    region = get_region_if_all_department_codes_belong_to_it(zone_codes)
    if region:
        return {
            "diffusion_zone_details": None,
            "diffusion_zone_details_display": region.name,
            "diffusion_zone_type": AdminDivisionType.REGION.value,
            "diffusion_zone_type_display": AdminDivisionType.REGION.label,
        }

    return {
        "diffusion_zone_details": None,
        "diffusion_zone_details_display": ", ".join(
            [
                diffusion_zone_info["diffusion_zone_details_display"]
                for zone_code in zone_codes
                if (
                    diffusion_zone_info := get_diffusion_zone_info_for_zone_code(
                        zone_code
                    )
                )
                and diffusion_zone_info["diffusion_zone_details_display"]
            ]
        ),
        "diffusion_zone_type": None,
        "diffusion_zone_type_display": "",
    }
