import json
import uuid

from django.core.management import call_command

from dora.core.test_utils import (
    make_emplois_orientation,
    make_jwt_orientation,
    make_orientation,
)


def _run_export(tmp_path):
    output = tmp_path / "export.json"
    call_command("export_emplois_orientations", "--output", str(output))
    with open(output, encoding="utf-8") as f:
        return json.load(f)


def test_exports_only_emplois_orientations(tmp_path):
    emplois_orientation = make_emplois_orientation()
    # Une orientation DORA classique (avec prescripteur) doit être exclue,
    make_orientation()
    # de même qu'une orientation JWT (données Emplois mais prescripteur DORA).
    make_jwt_orientation()

    data = _run_export(tmp_path)

    assert [entry["emplois_sync_uid"] for entry in data] == [
        str(emplois_orientation.emplois_orientation_data.emplois_sync_uid)
    ]


def test_linking_identifiers(tmp_path):
    orientation = make_emplois_orientation(emplois_data={"prescriber_id": uuid.uuid4()})
    emplois_data = orientation.emplois_orientation_data

    [entry] = _run_export(tmp_path)

    assert entry["emplois_sync_uid"] == str(emplois_data.emplois_sync_uid)
    assert entry["beneficiary_id"] == str(emplois_data.beneficiary_id)
    assert entry["prescriber_id"] == str(emplois_data.prescriber_id)
    assert entry["structure_id"] == str(emplois_data.structure_id)


def test_dora_service_identifier(tmp_path):
    orientation = make_emplois_orientation()

    [entry] = _run_export(tmp_path)

    assert entry["service_id"] == f"dora--{orientation.service_id}"


def test_di_service_identifier(tmp_path):
    make_emplois_orientation(service=None, di_service_id="di--abc")

    [entry] = _run_export(tmp_path)

    assert entry["service_id"] == "di--abc"


def test_includes_anonymized_orientations(tmp_path):
    # Une orientation anonymisée (données référent vidées) reste exportable :
    # les identifiants de réassociation ne sont pas anonymisés.
    orientation = make_emplois_orientation(
        is_anonymized=True,
        referent_first_name="",
        referent_last_name="",
        referent_email="",
    )

    [entry] = _run_export(tmp_path)

    assert entry["emplois_sync_uid"] == str(
        orientation.emplois_orientation_data.emplois_sync_uid
    )
    assert entry["referent_last_name"] == ""


def test_json_is_readable_with_consistent_count(tmp_path):
    make_emplois_orientation()
    make_emplois_orientation()

    data = _run_export(tmp_path)

    assert len(data) == 2
    assert all(entry["emplois_sync_uid"] for entry in data)
