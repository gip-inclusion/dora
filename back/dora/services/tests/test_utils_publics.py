from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.services.models import Public

FAMILLES = DiPublic.FAMILLES.value
ETUDIANTS = DiPublic.ETUDIANTS.value
ACTIFS = DiPublic.ACTIFS.value


def _public(name, slugs, structure=None):
    return baker.make(
        Public, name=name, structure=structure, corresponding_di_publics=slugs
    )
