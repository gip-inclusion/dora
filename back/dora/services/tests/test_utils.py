import pytest
from data_inclusion.schema.v1 import TypeService

from dora.core.test_utils import make_service
from dora.services.models import ServiceKind
from dora.services.utils import SERVICE_KIND_PRIORITY, compute_service_kind


def set_kinds(service, *values):
    service.kinds.set(ServiceKind.objects.filter(value__in=values))
    return service


def test_service_without_kinds_has_no_kind():
    assert compute_service_kind(make_service()) == ""


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

    assert compute_service_kind(service) == ""
