import re

from dora.admin_express.models import EPCI, City, Department

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


def get_zone_code_display(zone_code: str) -> str:
    if zone_code == "france":
        return "France entière"

    if re.match(r"^99[0-5]\d{2}$", zone_code):
        # Pays
        if zone_code == "99100":
            return "France entière"

    if re.match(r"^\w{5}$", zone_code):
        # Commune
        city = City.objects.get_from_code(zone_code)
        return f"{city.name} ({city.department})" if city else ""

    if re.match(r"^\w{2,3}$", zone_code):
        # Département
        department = Department.objects.get_from_code(zone_code)
        return department.name if department else ""

    if re.match(r"^\d{9}$", zone_code):
        # EPCI
        epci = EPCI.objects.get_from_code(zone_code)
        return epci.name if epci else ""

    return ""


def get_zone_codes_display(zone_codes: list[str]) -> list[str]:
    for region, departments in REGIONS_DEPARTEMENTS.items():
        if set(zone_codes) == departments:
            return region

    return ", ".join(
        [
            display
            for zone_code in zone_codes
            if (display := get_zone_code_display(zone_code))
        ]
    )
