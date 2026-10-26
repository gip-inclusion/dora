from io import StringIO
from unittest.mock import patch

import pytest
from django.conf import settings
from django.core.management import call_command

from dora.core.test_utils import make_model, make_service, make_structure
from dora.services.models import Service
from dora.services.utils import update_sync_checksum

BUCKET_OBJECTS = (
    "dora.services.management.commands.remove_dead_service_forms._iter_objects"
)


def key(structure, name):
    return f"{settings.ENVIRONMENT}/{structure.pk}/{name}"


def call_cmd(bucket_keys, **kwargs):
    with patch(BUCKET_OBJECTS, return_value=[(k, None) for k in bucket_keys]):
        call_command("remove_dead_service_forms", stdout=StringIO(), **kwargs)


@pytest.fixture
def structure():
    return make_structure()


def test_dry_run_does_not_write(structure):
    forms = [key(structure, "perdu.pdf"), key(structure, "present.pdf")]
    service = make_service(structure=structure, forms=list(forms))

    call_cmd([key(structure, "present.pdf")])

    service.refresh_from_db()
    assert forms == service.forms


def test_wet_run_removes_only_dead_managed_keys(structure):
    present = key(structure, "present.pdf")
    # Hors du périmètre du nettoyage : jamais supprimée par lui, donc laissée en l'état.
    unmanaged = "ailleurs/fichier.pdf"
    service = make_service(
        structure=structure, forms=[key(structure, "perdu.pdf"), present, unmanaged]
    )

    call_cmd([present], wet_run=True)

    service.refresh_from_db()
    assert [present, unmanaged] == service.forms


def test_wet_run_covers_models_and_realigns_synced_copies(structure):
    dead = key(structure, "perdu.pdf")
    present = key(structure, "present.pdf")
    model = make_model(structure=structure, forms=[dead, present])
    synced = make_service(
        model=model, forms=[dead, present], last_sync_checksum=model.sync_checksum
    )
    outdated = make_service(model=model, forms=[dead], last_sync_checksum="obsolete")

    call_cmd([present], wet_run=True)

    model = Service._base_manager.get(pk=model.pk)
    synced.refresh_from_db()
    outdated.refresh_from_db()

    assert [present] == model.forms
    assert [present] == synced.forms
    assert [] == outdated.forms
    assert model.sync_checksum == update_sync_checksum(model)
    # La copie à jour le reste, celle qui divergeait garde ses modifications en attente.
    assert model.sync_checksum == synced.last_sync_checksum
    assert "obsolete" == outdated.last_sync_checksum


def test_aborts_when_bucket_is_empty(structure):
    forms = [key(structure, "present.pdf")]
    service = make_service(structure=structure, forms=list(forms))

    call_cmd([], wet_run=True)

    service.refresh_from_db()
    assert forms == service.forms
