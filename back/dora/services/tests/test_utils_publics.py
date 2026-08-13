from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_service
from dora.services.models import Public
from dora.services.utils import TOUS_PUBLICS, compute_publics_di

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
