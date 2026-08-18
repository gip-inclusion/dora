import pytest
from data_inclusion.schema.v1 import TypeService
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.services.models import Public
from dora.services.utils import (
    SERVICE_KIND_PRIORITY,
    reduce_service_kinds,
)

FAMILLES = DiPublic.FAMILLES.value
ETUDIANTS = DiPublic.ETUDIANTS.value
ACTIFS = DiPublic.ACTIFS.value


def _public(name, slugs, structure=None):
    return baker.make(
        Public, name=name, structure=structure, corresponding_di_publics=slugs
    )


@pytest.mark.no_django_db
def test_no_kind_reduces_to_none():
    assert reduce_service_kinds([]) is None


@pytest.mark.no_django_db
@pytest.mark.parametrize("kind", [t.value for t in TypeService])
def test_single_kind_is_kept(kind):
    assert reduce_service_kinds([kind]) == kind


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "kinds,expected",
    [
        (["information", "aide-financiere"], "aide-financiere"),
        (["accompagnement", "aide-materielle"], "aide-materielle"),
        (["atelier", "formation"], "formation"),
        (["accompagnement", "atelier"], "atelier"),
        (["information", "accompagnement"], "accompagnement"),
        ([t.value for t in TypeService], "aide-financiere"),
    ],
)
def test_highest_priority_kind_wins(kinds, expected):
    assert reduce_service_kinds(kinds) == expected


@pytest.mark.no_django_db
def test_priority_covers_the_whole_referential():
    assert {k.value for k in SERVICE_KIND_PRIORITY} == {t.value for t in TypeService}


@pytest.mark.no_django_db
def test_kind_outside_the_referential_is_ignored():
    assert reduce_service_kinds(["obsolete"]) is None
