from io import StringIO

from data_inclusion.schema.v1.publics import Public as DiPublic
from django.core.management import call_command
from model_bakery import baker

from dora.core.test_utils import make_service, make_structure
from dora.services.models import Public, Service, ServiceModel

FAMILLES = DiPublic.FAMILLES.value


def _run(*args):
    out = StringIO()
    call_command("backfill_publics_di", *args, stdout=out)
    return out.getvalue()


def _service_with_drift():
    """Service dont la M2M résout [familles] mais dont la colonne stockée est volontairement fausse."""
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    # Contourne le signal de double écriture pour introduire un écart.
    Service.objects.filter(pk=service.pk).update(
        publics_di=["stale-value"], publics_precisions="stale"
    )
    return service


def test_dry_run_reports_drift_without_writing():
    service = _service_with_drift()

    out = _run()

    assert "à corriger" in out
    assert str(service.pk) in out

    service.refresh_from_db()
    assert service.publics_di == ["stale-value"]
    assert service.publics_precisions == "stale"


def test_run_fixes_drift():
    service = _service_with_drift()

    out = _run("--wet-run")

    assert "corrigés" in out
    service.refresh_from_db()
    assert service.publics_di == [FAMILLES]
    assert service.publics_precisions == "familles"


def test_clean_state_reports_no_drift():
    service = make_service()
    service.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )

    out = _run()

    assert "Aucun écart" in out
    service.refresh_from_db()
    assert service.publics_di == [FAMILLES]


def test_run_is_idempotent():
    _service_with_drift()

    _run("--wet-run")
    out = _run()

    assert "Aucun écart" in out


def test_fixes_service_model_with_drift():
    service_model_with_drift = baker.make(
        Service, is_model=True, structure=make_structure()
    )

    service_model_with_drift.publics.add(
        baker.make(Public, name="familles", corresponding_di_publics=[FAMILLES])
    )
    ServiceModel.objects.filter(pk=service_model_with_drift.pk).update(
        publics_di=["stale-value"], publics_precisions="stale"
    )

    out = _run("--wet-run")

    assert "corrigés" in out
    service_model_with_drift.refresh_from_db()
    assert service_model_with_drift.publics_di == [FAMILLES]
    assert service_model_with_drift.publics_precisions == "familles"
