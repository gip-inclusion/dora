import re
from collections import defaultdict

from unidecode import unidecode

from dora.decoupage_administratif.models import (
    EPCI,
    AdminDivisionType,
    City,
    Department,
    Region,
)

CODE_INSEE_PARIS = "75056"
CODE_INSEE_PARIS_ARRDTS = [
    "75101",
    "75102",
    "75103",
    "75104",
    "75105",
    "75106",
    "75107",
    "75108",
    "75109",
    "75110",
    "75111",
    "75112",
    "75113",
    "75114",
    "75115",
    "75116",
    "75117",
    "75118",
    "75119",
    "75120",
]
CODE_INSEE_LYON = "69123"
CODE_INSEE_LYON_ARRDTS = [
    "69381",
    "69382",
    "69383",
    "69384",
    "69385",
    "69386",
    "69387",
    "69388",
    "69389",
]
CODE_INSEE_MARSEILLE = "13055"
CODE_INSEE_MARSEILLE_ARRDTS = [
    "13201",
    "13202",
    "13203",
    "13204",
    "13205",
    "13206",
    "13207",
    "13208",
    "13209",
    "13210",
    "13211",
    "13212",
    "13213",
    "13214",
    "13215",
    "13216",
]


def arrdt_to_main_insee_code(insee_code):
    if insee_code in CODE_INSEE_PARIS_ARRDTS:
        return CODE_INSEE_PARIS
    if insee_code in CODE_INSEE_LYON_ARRDTS:
        return CODE_INSEE_LYON
    if insee_code in CODE_INSEE_MARSEILLE_ARRDTS:
        return CODE_INSEE_MARSEILLE
    return insee_code


def main_insee_code_to_arrdts(insee_code):
    if insee_code == CODE_INSEE_PARIS:
        return CODE_INSEE_PARIS_ARRDTS
    if insee_code == CODE_INSEE_LYON:
        return CODE_INSEE_LYON_ARRDTS
    if insee_code == CODE_INSEE_MARSEILLE:
        return CODE_INSEE_MARSEILLE_ARRDTS
    return [insee_code]


def normalize_string_for_search(str):
    return unidecode(str).upper().replace("-", " ").replace("’", "'").rstrip()


def get_clean_city_name(insee_code):
    if insee_code:
        city = City.objects.get_from_code(arrdt_to_main_insee_code(insee_code))
        if city:
            return city.name
    return ""


FRANCE_INSEE_CODE = "99100"

# Format des codes de divisions administratives. Les longueurs sont disjointes :
# un code n'a donc jamais qu'un seul type possible.
COUNTRY_CODE_PATTERN = r"^99[0-5]\d{2}$"
CITY_CODE_PATTERN = r"^\w{5}$"
DEPARTMENT_CODE_PATTERN = r"^\w{2,3}$"
EPCI_CODE_PATTERN = r"^\d{9}$"
REGION_CODE_PATTERN = r"^\w{2}$"

CODE_PATTERN_BY_TYPE = {
    AdminDivisionType.EPCI: EPCI_CODE_PATTERN,
    AdminDivisionType.CITY: CITY_CODE_PATTERN,
    AdminDivisionType.DEPARTMENT: DEPARTMENT_CODE_PATTERN,
}

MODEL_BY_TYPE = {
    AdminDivisionType.EPCI: EPCI,
    AdminDivisionType.CITY: City,
    AdminDivisionType.DEPARTMENT: Department,
}


def group_codes_by_division_type(codes):
    """Répartit des codes par type de division, d'après leur seul format."""
    grouped = defaultdict(set)
    for code in codes:
        for division_type, pattern in CODE_PATTERN_BY_TYPE.items():
            if re.match(pattern, code):
                grouped[division_type].add(code)
                break
    return grouped


def get_zone_eligibilite_choices(codes):
    """Reconstitue les territoires sélectionnés à partir des codes enregistrés.

    `zone_eligibilite` ne contient que des codes, sans leur type : le format du
    code permet de le déduire (9 chiffres pour un EPCI, 5 caractères pour une
    commune, 2 ou 3 pour un département). Une région ayant été enregistrée sous
    la forme de l'ensemble de ses départements, on ne la reconstitue que si tous
    y figurent.

    Renvoie une liste de `{"label", "type", "codes"}`, directement exploitable
    par le champ de recherche du formulaire. Les libellés suivent le même format
    que les résultats de recherche, pour qu'un territoire déjà enregistré
    s'affiche exactement comme s'il venait d'être choisi.
    """
    if not codes:
        return []

    grouped = group_codes_by_division_type(codes)
    divisions = {
        division_type: {
            division.code: division
            for division in MODEL_BY_TYPE[division_type].objects.filter(
                code__in=division_codes
            )
        }
        for division_type, division_codes in grouped.items()
    }

    departments = divisions.get(AdminDivisionType.DEPARTMENT, {})
    department_codes = set(departments)

    choices = []
    if department_codes:
        codes_by_region = defaultdict(set)
        for code, region_code in Department.objects.values_list("code", "region"):
            codes_by_region[region_code].add(code)

        regions = Region.objects.filter(
            code__in={department.region for department in departments.values()}
        ).order_by("name")
        for region in regions:
            region_codes = codes_by_region[region.code]
            # une région d'un seul département est indiscernable de ce
            # département : on garde alors le département, plus littéral
            if len(region_codes) > 1 and region_codes <= department_codes:
                choices.append(
                    {
                        "label": region.name,
                        "type": AdminDivisionType.REGION,
                        "codes": sorted(region_codes),
                    }
                )
                department_codes -= region_codes

    choices += [
        {
            "label": f"{departments[code].name} ({code})",
            "type": AdminDivisionType.DEPARTMENT,
            "codes": [code],
        }
        for code in sorted(department_codes)
    ]
    epcis = divisions.get(AdminDivisionType.EPCI, {})
    choices += [
        {
            "label": epcis[code].name,
            "type": AdminDivisionType.EPCI,
            "codes": [code],
        }
        for code in sorted(epcis)
    ]
    cities = divisions.get(AdminDivisionType.CITY, {})
    choices += [
        {
            "label": f"{cities[code].name} ({code})",
            "type": AdminDivisionType.CITY,
            "codes": [code],
        }
        for code in sorted(cities)
    ]

    return choices
