import pytest
from model_bakery.random_gen import gen_email

from dora.core.test_utils import make_orientation

from ..models import Orientation


@pytest.fixture
def orientation() -> Orientation:
    # l'e-mail bénéficiaire est optionel dans la génération,
    # mais on veut vérifier l'envoi d'e-mail vers tous les destinataires
    return make_orientation(beneficiary_email=gen_email)
