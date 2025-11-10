import re

from dora.admin_express.models import EPCI, AdminDivisionType, City, Department

REGIONS_DEPARTEMENTS = {
    "Guadeloupe": {"971"},
    "Martinique": {"972"},
    "Guyane": {"973"},
    "La Réunion": {"974"},
    "Mayotte": {"976"},
    "Île-de-France": {
        "75",
        "77",
        "78",
        "91",
        "92",
        "93",
        "94",
        "95",
    },
    "Centre-Val de Loire": {
        "18",
        "28",
        "36",
        "37",
        "41",
        "45",
    },
    "Bourgogne-Franche-Comté": {
        "21",
        "25",
        "39",
        "58",
        "70",
        "71",
        "89",
        "90",
    },
    "Normandie": {
        "14",
        "27",
        "50",
        "61",
        "76",
    },
    "Hauts-de-France": {
        "02",
        "59",
        "60",
        "62",
        "80",
    },
    "Grand Est": {
        "08",
        "10",
        "51",
        "52",
        "54",
        "55",
        "57",
        "67",
        "68",
        "88",
    },
    "Pays de la Loire": {
        "44",
        "49",
        "53",
        "72",
        "85",
    },
    "Bretagne": {
        "22",
        "29",
        "35",
        "56",
    },
    "Nouvelle-Aquitaine": {
        "16",
        "17",
        "19",
        "23",
        "24",
        "33",
        "40",
        "47",
        "64",
        "79",
        "86",
        "87",
    },
    "Occitanie": {
        "09",
        "11",
        "12",
        "30",
        "31",
        "32",
        "34",
        "46",
        "48",
        "65",
        "66",
        "81",
        "82",
    },
    "Auvergne-Rhône-Alpes": {
        "01",
        "03",
        "07",
        "15",
        "26",
        "38",
        "42",
        "43",
        "63",
        "69",
        "73",
        "74",
    },
    "Provence-Alpes-Côte d'Azur": {
        "04",
        "05",
        "06",
        "13",
        "83",
        "84",
    },
    "Corse": {
        "2A",
        "2B",
    },
}


def get_diffusion_zone_info_for_zone_code(zone_code: str) -> dict:
    if zone_code == "france":
        return {
            "diffusion_zone_details": None,
            "diffusion_zone_details_display": "France entière",
            "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
            "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
        }

    if re.match(r"^99[0-5]\d{2}$", zone_code):
        # Pays
        if zone_code == "99100":
            return {
                "diffusion_zone_details": None,
                "diffusion_zone_details_display": "France entière",
                "diffusion_zone_type": AdminDivisionType.COUNTRY.value,
                "diffusion_zone_type_display": AdminDivisionType.COUNTRY.label,
            }

    if re.match(r"^\w{5}$", zone_code):
        # Commune
        city = City.objects.get_from_code(zone_code)
        if city:
            return {
                "diffusion_zone_details": city.code,
                "diffusion_zone_details_display": f"{city.name} ({city.department})",
                "diffusion_zone_type": AdminDivisionType.CITY.value,
                "diffusion_zone_type_display": AdminDivisionType.CITY.label,
            }

    if re.match(r"^\w{2,3}$", zone_code):
        # Département
        department = Department.objects.get_from_code(zone_code)
        if department:
            return {
                "diffusion_zone_details": department.code,
                "diffusion_zone_details_display": department.name,
                "diffusion_zone_type": AdminDivisionType.DEPARTMENT.value,
                "diffusion_zone_type_display": AdminDivisionType.DEPARTMENT.label,
            }

    if re.match(r"^\d{9}$", zone_code):
        # EPCI
        epci = EPCI.objects.get_from_code(zone_code)
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


def get_diffusion_zone_info(zone_codes: list[str]) -> list[str]:
    for region, departments in REGIONS_DEPARTEMENTS.items():
        if set(zone_codes) == departments:
            return {
                "diffusion_zone_details": None,
                "diffusion_zone_details_display": region,
                "diffusion_zone_type": AdminDivisionType.REGION.value,
                "diffusion_zone_type_display": AdminDivisionType.REGION.label,
            }

    if len(zone_codes) == 1:
        return get_diffusion_zone_info_for_zone_code(zone_codes[0])

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
