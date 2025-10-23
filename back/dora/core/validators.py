import re
from itertools import chain

from django.core.exceptions import ValidationError
from osm_time import ParseException
from osm_time.opening_hours import OpeningHours

from .constants import SIREN_LA_POSTE


# From: https://github.com/betagouv/itou/blob/master/itou/utils/validators.py
def validate_siret(siret):
    if not siret.isdigit() or len(siret) != 14:
        raise ValidationError("Le numéro SIRET doit être composé de 14 chiffres.")


def validate_opening_hours_str(opening_hours_str):
    try:
        OpeningHours(opening_hours_str)
    except ParseException:
        raise ValidationError("Le format des horaires d’ouverture est incorrect")


def validate_accesslibre_url(url):
    if url and not url.startswith("https://acceslibre.beta.gouv.fr/"):
        raise ValidationError("L’URL doit débuter par https://acceslibre.beta.gouv.fr/")


def validate_safir(safir):
    if not safir.isdigit() or len(safir) != 5:
        raise ValidationError("Le code SAFIR doit être composé de 5 chiffres.")


def _validation_key(siren_or_siret):
    # calcul de validité du SIREN et SIRET
    # voir : https://www.sirene.fr/static-resources/doc/lettres/lettre-16-novembre-2013.pdf

    tmp = siren_or_siret[::-1]
    even = [int(d) for d in tmp[::2]]
    odd = [str(2 * int(d)) for d in tmp[1::2]]

    # décompose les nombres supérieurs à 9 en chiffres
    odd = list(map(int, chain(*odd)))

    # pour être valide, la clé doit être un multiple de 10
    return sum([*even, *odd])


def validate_siren(siren):
    if not siren.isdigit() or len(siren) != 9:
        raise ValidationError("Le numéro SIREN doit être composé de 9 chiffres.")

    key = _validation_key(siren)

    if key % 10:
        raise ValidationError(f"Le numéro SIREN est incorrect (clé: {key}).")


def validate_full_siret(siret):
    validate_siret(siret)

    # les SIRET peuvent être validés comme les SIREN,
    # sauf pour les agences de la Poste

    if siret.startswith(SIREN_LA_POSTE):
        # cas particulier de La Poste : la somme des chiffres du SIRET doit être un multiple de 5
        key = sum([int(d) for d in siret])
        if key % 5:
            raise ValidationError(f"Le numéro SIRET est incorrect (clé: {key}).")
        return

    key = _validation_key(siret)

    if key % 10:
        raise ValidationError(f"Le numéro SIRET est incorrect (clé: {key}).")


def validate_phone_number(phone_number: str):
    # simpliste, mais première vérification utile pour les imports
    # format national (0xxxxxxxxx)
    if len(phone_number) > 10:
        raise ValidationError(f"Le numéro de téléphone {phone_number} est incorrect.")

    if len(phone_number) == 10 and phone_number[0] != "0":
        raise ValidationError(
            "Un numéro de téléphone à 10 chiffres doit commencer par 0"
        )

    if phone_number:
        try:
            int(phone_number)
        except ValueError:
            raise ValidationError(
                f"Le numéro de téléphone {phone_number} ne contient pas que des chiffres"
            )


def validate_version(value: str):
    """
    Assurer qu'une version est dans le format <int>.<int> comme 2.1 ou 10.52
    """
    if not re.match(r"^\d+\.\d+$", value):
        raise ValidationError("La version doit être dans le format <int>.<int>")
