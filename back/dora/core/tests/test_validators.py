import pytest
from django.core.exceptions import ValidationError

from ..constants import SIREN_FRANCE_TRAVAIL, SIREN_LA_POSTE
from ..validators import validate_full_siret, validate_phone_number, validate_siren


def test_validate_siren():
    # SIREN de l'INSEE
    validate_siren("120027016")

    # SIREN de La Poste (attention aux SIRET des agences)
    validate_siren(SIREN_LA_POSTE)

    # SIREN FT / PE
    validate_siren(SIREN_FRANCE_TRAVAIL)

    with pytest.raises(ValidationError, match="Le numéro SIREN est incorrect"):
        # SIREN exemple
        validate_siren("123456789")


def test_validate_siret_full():
    # agence FT Paris 18
    validate_full_siret("13000548121800")

    with pytest.raises(ValidationError, match="Le numéro SIRET est incorrect"):
        # un SIRET incorrect basé sur le SIREN FT / PE
        validate_full_siret(SIREN_FRANCE_TRAVAIL + "12345")


def test_validate_siret_full_la_poste():
    # Agence La Poste - Paris 1er Les Halles
    validate_full_siret(SIREN_LA_POSTE + "37187")

    with pytest.raises(ValidationError, match="Le numéro SIRET est incorrect"):
        # un SIRET incorrect basé sur le SIREN La Poste
        validate_full_siret(SIREN_LA_POSTE + "12345")


def test_validate_phone_number():
    # numéro court
    validate_phone_number("3698")

    # numéro "standard"
    validate_phone_number("0600003698")

    # numéro vide
    validate_phone_number("")

    with pytest.raises(
        ValidationError,
        match="Un numéro de téléphone à 10 chiffres doit commencer par 0",
    ):
        validate_phone_number("1234567890")

    with pytest.raises(ValidationError, match="incorrect"):
        validate_phone_number("12345678901")

    with pytest.raises(ValidationError, match="ne contient pas que des chiffres"):
        validate_phone_number("1x")
