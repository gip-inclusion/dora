import csv

import pytest
from django.core.management import call_command
from model_bakery import baker

from dora.core.test_utils import (
    make_model,
    make_published_service,
    make_service,
    make_structure,
)
from dora.services.management.commands.merge_service_descriptions import (
    needs_merge,
    pair_hash,
)
from dora.services.models import Service
from dora.services.utils import instantiate_service_from_model, update_sync_checksum


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "short_desc,description,expected",
    [
        ("Un résumé", "Un résumé", False),
        # le résumé est saisi en texte brut, le descriptif en markdown
        ("Un résumé", "**Un résumé** mis en forme", False),
        ("Un résumé", "un   RÉSUMÉ\n\nsuivi d'un développement", False),
        ("Un résumé", "Un tout autre descriptif", True),
    ],
)
def test_needs_merge(short_desc, description, expected):
    assert needs_merge(short_desc, description) is expected


def test_service_exposes_description_and_its_alias(api_client):
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    assert api_client.get(f"/services/{service.slug}/").data["full_desc"] == "Avant"

    response = api_client.patch(f"/services/{service.slug}/", {"full_desc": "Après"})

    assert response.status_code == 200
    service.refresh_from_db()
    assert service.description == "Après"


def test_alias_takes_precedence_over_description(api_client):
    # Ce que poste un front non basculé : il édite `full_desc` et réexpédie tel quel le
    # `description` reçu au chargement. Retenir ce dernier annulerait la modification.
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    service = make_published_service(structure=structure, description="Avant")
    api_client.force_authenticate(user=user)

    api_client.patch(
        f"/services/{service.slug}/",
        {"full_desc": "Après", "description": "Avant"},
    )

    service.refresh_from_db()
    assert service.description == "Après"


def _merge(tmp_path, *args):
    call_command(
        "merge_service_descriptions",
        *args,
        "--output",
        str(tmp_path / "restants.csv"),
    )
    path = tmp_path / "restants.csv"
    return list(csv.DictReader(path.open(encoding="utf-8"))) if path.exists() else []


def _write_merges(path, merges):
    with path.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["pair_hash", "description"])
        writer.writeheader()
        writer.writerows(merges)


def test_merge_copies_short_desc_when_description_is_empty(tmp_path):
    service = make_service(short_desc="Un résumé", description="")
    modification_date = service.modification_date

    _merge(tmp_path, "--wet-run")

    service.refresh_from_db()
    assert service.description == "Un résumé"
    # la date de modification pilote les rappels « service à actualiser »
    assert service.modification_date == modification_date


def test_merge_dry_run_writes_nothing(tmp_path):
    service = make_service(short_desc="Un résumé", description="")

    _merge(tmp_path)

    service.refresh_from_db()
    assert service.description == ""


def test_merge_exports_one_pair_per_distinct_values(tmp_path):
    structure = make_structure()
    for _ in range(2):
        make_service(
            structure=structure, short_desc="Un résumé", description="Un descriptif"
        )
    make_service(
        structure=structure,
        short_desc="Autre résumé",
        description="Un tout autre texte",
    )
    # déjà couverts par leur description, à ne pas exporter
    make_service(structure=structure, short_desc="Seul", description="")
    make_service(
        structure=structure, short_desc="Repris", description="Repris tel quel"
    )

    rows = _merge(tmp_path, "--wet-run")

    assert {row["short_desc"]: int(row["nb_services"]) for row in rows} == {
        "Un résumé": 2,
        "Autre résumé": 1,
    }


def test_merge_applies_merges_from_csv(tmp_path):
    service = make_service(short_desc="Un résumé", description="Un descriptif")
    merges = tmp_path / "fusions.csv"
    _write_merges(
        merges,
        [
            {
                "pair_hash": pair_hash("Un résumé", "Un descriptif"),
                "description": "Un résumé fusionné au descriptif",
            }
        ],
    )

    _merge(tmp_path, "--from-csv", str(merges), "--wet-run")

    service.refresh_from_db()
    assert service.description == "Un résumé fusionné au descriptif"


def test_merge_skips_services_changed_since_export(tmp_path):
    service = make_service(short_desc="Un résumé", description="Descriptif réécrit")
    merges = tmp_path / "fusions.csv"
    _write_merges(
        merges,
        [
            {
                "pair_hash": pair_hash("Un résumé", "Descriptif d'origine"),
                "description": "Fusion périmée",
            }
        ],
    )

    rows = _merge(tmp_path, "--from-csv", str(merges), "--wet-run")

    service.refresh_from_db()
    assert service.description == "Descriptif réécrit"
    assert [row["description"] for row in rows] == ["Descriptif réécrit"]


def test_merge_keeps_copies_in_sync(tmp_path):
    structure = make_structure(baker.make("users.User", is_valid=True))
    model = make_model(
        structure=structure, short_desc="Un résumé", description="Un descriptif"
    )
    synced = instantiate_service_from_model(model, structure, structure.creator)
    customized = instantiate_service_from_model(model, structure, structure.creator)
    Service._base_manager.filter(pk=customized.pk).update(last_sync_checksum="périmé")

    merges = tmp_path / "fusions.csv"
    _write_merges(
        merges,
        [
            {
                "pair_hash": pair_hash("Un résumé", "Un descriptif"),
                "description": "Un descriptif, résumé compris",
            }
        ],
    )

    _merge(tmp_path, "--from-csv", str(merges), "--wet-run")

    model.refresh_from_db()
    synced.refresh_from_db()
    customized.refresh_from_db()
    # même fusion pour le modèle et ses copies : aucune ne doit passer en « modifié »…
    assert synced.description == model.description == "Un descriptif, résumé compris"
    assert model.sync_checksum == update_sync_checksum(model)
    assert synced.last_sync_checksum == model.sync_checksum
    # … et celles qui l'étaient déjà le restent
    assert customized.last_sync_checksum == "périmé"
