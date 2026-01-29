from unidecode import unidecode

from dora.decoupage_administratif.models import City

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
    return unidecode(str).upper().replace("-", " ").replace("'", "'").rstrip()


def get_clean_city_name(insee_code):
    if insee_code:
        city = City.objects.get_from_code(arrdt_to_main_insee_code(insee_code))
        if city:
            return city.name
    return ""
