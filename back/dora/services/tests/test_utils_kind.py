import pytest
from data_inclusion.schema.v1 import TypeService
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_service
from dora.services.models import Public, ServiceKind
from dora.services.utils import (
    PRECISIONS_MAX_LENGTH,
    SERVICE_KIND_PRIORITY,
    TOUS_PUBLICS,
    compute_publics_di,
    compute_service_kind,
)

FAMILLES = DiPublic.FAMILLES.value
ETUDIANTS = DiPublic.ETUDIANTS.value
ACTIFS = DiPublic.ACTIFS.value


def _public(name, slugs, structure=None):
    return baker.make(
        Public, name=name, structure=structure, corresponding_di_publics=slugs
    )


def test_empty_m2m_returns_empty():
    # [] signifie « tous publics »
    service = make_service()
    assert compute_publics_di(service) == []


def test_single_public():
    service = make_service()
    service.publics.add(_public("familles", [FAMILLES]))
    assert compute_publics_di(service) == [FAMILLES]


def test_publics_di_contains_only_unique_values():
    service = make_service()
    service.publics.add(
        _public("a", [FAMILLES, ETUDIANTS]),
        _public("b", [ETUDIANTS, ACTIFS]),
    )
    publics_di = compute_publics_di(service)
    assert publics_di == sorted({ACTIFS, ETUDIANTS, FAMILLES})


def test_exclusivity_drops_tous_publics_if_another_public_present():
    service = make_service()
    service.publics.add(
        _public("tous", [TOUS_PUBLICS]),
        _public("familles", [FAMILLES]),
    )
    assert compute_publics_di(service) == [FAMILLES]


def test_tous_publics_is_never_stored():
    # tous-publics est toujours retiré : un service « tous publics » stocke [].
    service = make_service()
    service.publics.add(_public("tous", [TOUS_PUBLICS]))
    assert compute_publics_di(service) == []


def test_invalid_slug_filtered_out():
    service = make_service()
    public = _public("familles", [FAMILLES])
    service.publics.add(public)
    Public.objects.filter(pk=public.pk).update(
        corresponding_di_publics=["not-a-real-public", FAMILLES]
    )
    assert compute_publics_di(service) == [FAMILLES]


def test_publics_di_is_sorted():
    service = make_service()
    service.publics.add(
        _public("z", [FAMILLES]),
        _public("a", [ACTIFS]),
    )
    publics_di = compute_publics_di(service)
    assert publics_di == sorted(publics_di)


def test_publics_precisions_empty_if_exceeds_limit():
    service = make_service()
    for i in range(PRECISIONS_MAX_LENGTH + 1):
        service.publics.add(_public(str(i), [FAMILLES], structure=make_structure()))

    _, precisions = compute_publics_di(service)
    assert precisions == ""


def set_kinds(service, *values):
    service.kinds.set(ServiceKind.objects.filter(value__in=values))
    return service


def test_service_without_kinds_has_no_kind():
    assert compute_service_kind(make_service()) is None


@pytest.mark.parametrize("kind", [t.value for t in TypeService])
def test_single_kind_is_kept(kind):
    assert compute_service_kind(set_kinds(make_service(), kind)) == kind


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
    assert compute_service_kind(set_kinds(make_service(), *kinds)) == expected


def test_priority_covers_the_whole_referential():
    assert {k.value for k in SERVICE_KIND_PRIORITY} == {t.value for t in TypeService}


def test_kind_outside_the_referential_is_ignored():
    kind = ServiceKind.objects.create(value="obsolete", label="Obsolète")
    service = make_service()
    service.kinds.set([kind])

    assert compute_service_kind(service) is None
