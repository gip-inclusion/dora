import pytest
from model_bakery.random_gen import gen_email

from dora.core.test_utils import (
    make_di_orientation,
    make_emplois_orientation,
    make_jwt_orientation,
    make_orientation,
)

from ..models import Orientation


@pytest.fixture(
    params=[make_orientation, make_jwt_orientation, make_emplois_orientation],
    ids=["dora", "jwt", "emplois"],
)
def orientation(request) -> Orientation:
    # l'e-mail bénéficiaire est optionel dans la génération,
    # mais on veut vérifier l'envoi d'e-mail vers tous les destinataires
    return request.param(beneficiary_email=gen_email())


@pytest.fixture
def di_orientation() -> Orientation:
    # l'e-mail bénéficiaire est optionel dans la génération,
    # mais on veut vérifier l'envoi d'e-mail vers tous les destinataires
    return make_di_orientation(beneficiary_email=gen_email)
