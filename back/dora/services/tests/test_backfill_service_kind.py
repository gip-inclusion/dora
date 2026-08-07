from django.core.management import call_command

from dora.core.test_utils import make_model, make_service
from dora.services.models import Service, ServiceKind


def desynchronise(service, kind):
    """Écrit `kind` en base sans passer par la double écriture."""
    Service._base_manager.filter(pk=service.pk).update(kind=kind)


def set_kinds(service, *values):
    service.kinds.set(ServiceKind.objects.filter(value__in=values))
    return service


def reloaded_kind(service):
    return Service._base_manager.get(pk=service.pk).kind


def test_fixes_diverging_kinds():
    service = set_kinds(make_service(), "formation")
    desynchronise(service, "information")

    call_command("backfill_service_kind", "--wet-run")

    assert reloaded_kind(service) == "formation"


def test_dry_run_fixes_nothing():
    service = set_kinds(make_service(), "formation")
    desynchronise(service, "information")

    call_command("backfill_service_kind")

    assert reloaded_kind(service) == "information"


def test_leaves_synchronized_services_untouched():
    service = set_kinds(make_service(), "formation")

    call_command("backfill_service_kind", "--wet-run")

    assert reloaded_kind(service) == "formation"


def test_fixes_service_models_too():
    # `Service.objects` exclut les modèles : la réconciliation passe par `_base_manager`
    model = set_kinds(make_model(), "atelier")
    desynchronise(model, "")

    call_command("backfill_service_kind", "--wet-run")

    assert reloaded_kind(model) == "atelier"


def test_clears_the_kind_of_a_service_without_kinds():
    service = make_service()
    desynchronise(service, "formation")

    call_command("backfill_service_kind", "--wet-run")

    assert reloaded_kind(service) == ""
