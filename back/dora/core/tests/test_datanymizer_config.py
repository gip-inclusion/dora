"""
Garde-fou pour `back/tools/datanymizer-config.yml`.

Échoue dès qu'un modèle ou champ potentiellement porteur de PII n'est pas
couvert par une règle d'anonymisation, exclu via `filter.except`, ou déclaré
comme faux positif dans `PII_FIELD_FALSE_POSITIVES`.
"""

import re
from pathlib import Path

import pytest
import yaml
from django.apps import apps

DATANYMIZER_CONFIG_PATH = (
    Path(__file__).resolve().parents[3] / "tools" / "datanymizer-config.yml"
)

# Champs dont le nom évoque du PII : exactement le mot, ou suffixe `_<mot>`.
PII_FIELD_PATTERN = re.compile(
    r"(^|_)("
    r"email|phone|telephone|first_name|last_name|contact_name|"
    r"ip_address|sub_pc|password|address\d*|adresse\d*"
    r")$"
)

# Champs qui matchent le motif mais ne contiennent pas de PII en pratique.
# Format : "<db_table>.<field_name>".
PII_FIELD_FALSE_POSITIVES: set[str] = {
    # Adresses postales institutionnelles (structures, services, SIRENE) :
    # ne relèvent pas du PII au sens strict.
    "structures_structure.address1",
    "structures_structure.address2",
    "services_service.address1",
    "services_service.address2",
    "sirene_establishment.address1",
    "sirene_establishment.address2",
}

# Tables Django/PostGIS qu'on peut légitimement exclure mais qui ne sont
# pas découvertes par `apps.get_models()`.
EXTRA_KNOWN_TABLES = {
    "django_admin_log",
    "django_session",
    "authtoken_token",
    "spatial_ref_sys",
}


@pytest.fixture(scope="module")
def datanymizer_config() -> dict:
    with DATANYMIZER_CONFIG_PATH.open() as fh:
        return yaml.safe_load(fh)


def _excluded_tables(config: dict) -> set[str]:
    return {
        entry.split(".", 1)[-1]
        for entry in (config.get("filter") or {}).get("except") or []
    }


def _all_known_tables() -> set[str]:
    tables = set()
    for model in apps.get_models():
        tables.add(model._meta.db_table)
        # Les tables intermédiaires M2M auto-générées par Django ne sont
        # pas listées dans `apps.get_models()`.
        for m2m in model._meta.local_many_to_many:
            if (through := m2m.remote_field.through) is not None:
                tables.add(through._meta.db_table)
    return tables | EXTRA_KNOWN_TABLES


def test_datanymizer_config_covers_pii_fields(datanymizer_config):
    excluded = _excluded_tables(datanymizer_config)
    rules_by_table = {
        entry["name"]: set((entry.get("rules") or {}).keys())
        for entry in datanymizer_config.get("tables") or []
    }

    uncovered: set[str] = set()
    for model in apps.get_models():
        table = model._meta.db_table
        if table in excluded:
            continue
        for field in model._meta.fields:
            qualified = f"{table}.{field.name}"
            if (
                PII_FIELD_PATTERN.search(field.name)
                and field.name not in rules_by_table.get(table, set())
                and qualified not in PII_FIELD_FALSE_POSITIVES
            ):
                uncovered.add(qualified)

    assert not uncovered, (
        f"Champs PII non couverts dans {DATANYMIZER_CONFIG_PATH.name} :\n"
        + "\n".join(f"  - {entry}" for entry in sorted(uncovered))
        + "\n\nSolutions : ajouter une règle d'anonymisation, exclure la "
        "table via `filter.except`, ou ajouter `<table>.<field>` à "
        "`PII_FIELD_FALSE_POSITIVES` si ce n'est pas du PII."
    )


def test_datanymizer_referenced_tables_exist(datanymizer_config):
    known = _all_known_tables()

    bad = [
        f"filter.except: {entry}"
        for entry in sorted(_excluded_tables(datanymizer_config) - known)
    ] + [
        f"tables[].name: {entry['name']}"
        for entry in datanymizer_config.get("tables") or []
        if entry["name"] not in known
    ]

    assert not bad, (
        "Entrées qui ne correspondent à aucune table connue (typo ?) :\n"
        + "\n".join(f"  - {entry}" for entry in bad)
    )
