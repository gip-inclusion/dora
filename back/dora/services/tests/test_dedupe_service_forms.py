from io import StringIO
from unittest.mock import patch

import pytest
from django.core.management import call_command

from dora.core.test_utils import make_model, make_service, make_structure
from dora.services.models import Service
from dora.services.utils import update_sync_checksum


def call_cmd(**kwargs):
    call_command("dedupe_service_forms", stdout=StringIO(), **kwargs)


@pytest.mark.django_db
def test_dry_run_does_not_write():
    service = make_service(forms=["prod/42/dossier.pdf", "prod/42/dossier.pdf"])

    call_cmd()

    service.refresh_from_db()
    assert ["prod/42/dossier.pdf", "prod/42/dossier.pdf"] == service.forms


@pytest.mark.django_db
def test_wet_run_removes_exact_duplicates():
    service = make_service(
        forms=[
            "prod/42/dossier.pdf",
            "prod/42/attestation.pdf",
            "prod/42/dossier.pdf",
        ]
    )

    call_cmd(wet_run=True)

    service.refresh_from_db()
    assert ["prod/42/dossier.pdf", "prod/42/attestation.pdf"] == service.forms


@pytest.mark.django_db
def test_wet_run_keeps_distinct_keys_sharing_a_file_name():
    # Deux clés distinctes désignent deux fichiers différents : les départager n'appartient
    # pas à la commande, qui se contente de les signaler.
    forms = ["prod/42/dossier.pdf", "prod/51/dossier.pdf"]
    service = make_service(forms=list(forms))

    call_cmd(wet_run=True)

    service.refresh_from_db()
    assert forms == service.forms


@pytest.mark.django_db
def test_wet_run_realigns_model_checksum_and_synced_copies():
    model = make_model(forms=["prod/42/dossier.pdf", "prod/42/dossier.pdf"])
    synced = make_service(
        model=model,
        forms=["prod/42/dossier.pdf"],
        last_sync_checksum=model.sync_checksum,
    )
    outdated = make_service(
        model=model, forms=["prod/42/dossier.pdf"], last_sync_checksum="obsolete"
    )

    call_cmd(wet_run=True)

    model.refresh_from_db()
    synced.refresh_from_db()
    outdated.refresh_from_db()

    assert ["prod/42/dossier.pdf"] == model.forms
    assert model.sync_checksum == update_sync_checksum(model)
    # La copie à jour le reste, celle qui divergeait garde ses modifications en attente.
    assert model.sync_checksum == synced.last_sync_checksum
    assert "obsolete" == outdated.last_sync_checksum


@pytest.mark.django_db
def test_wet_run_covers_models_and_services():
    structure = make_structure()
    model = make_model(structure=structure, forms=["prod/42/a.pdf", "prod/42/a.pdf"])
    service = make_service(structure=structure, forms=["prod/42/b.pdf"] * 3)

    call_cmd(wet_run=True)

    assert ["prod/42/a.pdf"] == Service._base_manager.get(pk=model.pk).forms
    assert ["prod/42/b.pdf"] == Service._base_manager.get(pk=service.pk).forms


@pytest.mark.django_db
def test_wet_run_writes_nothing_when_a_write_fails():
    model = make_model(forms=["prod/42/dossier.pdf", "prod/42/dossier.pdf"])
    synced = make_service(
        model=model,
        forms=["prod/42/dossier.pdf"],
        last_sync_checksum=model.sync_checksum,
    )
    initial_checksum = model.sync_checksum

    # La seconde écriture (les empreintes des modèles) échoue : la première doit être
    # défaite avec elle, sinon `forms` perdrait ses doublons sans que l'empreinte suive.
    bulk_update = Service._base_manager.bulk_update
    calls = []

    def failing_bulk_update(*args, **kwargs):
        calls.append(args)
        if len(calls) > 1:
            raise RuntimeError("échec simulé")
        return bulk_update(*args, **kwargs)

    with patch.object(
        Service._base_manager, "bulk_update", side_effect=failing_bulk_update
    ):
        with pytest.raises(RuntimeError):
            call_cmd(wet_run=True)

    model.refresh_from_db()
    synced.refresh_from_db()
    assert ["prod/42/dossier.pdf", "prod/42/dossier.pdf"] == model.forms
    assert initial_checksum == model.sync_checksum
    assert initial_checksum == synced.last_sync_checksum
