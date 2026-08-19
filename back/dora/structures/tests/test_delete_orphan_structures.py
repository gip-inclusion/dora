from datetime import timedelta

import pytest
from django.core.management import call_command
from model_bakery import baker

from dora.core.models import LogItem
from dora.core.test_utils import (
    make_service,
    make_structure,
    make_structure_member,
    make_user,
)
from dora.structures.management.commands.delete_orphan_structures import CREATED_BEFORE
from dora.structures.models import (
    Structure,
    StructureNationalLabel,
    StructurePutativeMember,
)


def make_orphan_structure(created_at=CREATED_BEFORE - timedelta(days=1), **kwargs):
    # `creation_date` est en `auto_now_add`, on ne peut la fixer qu'après coup
    structure = make_structure(**kwargs)
    Structure.objects.filter(pk=structure.pk).update(creation_date=created_at)
    return structure


def test_deletes_orphan_structures():
    structure = make_orphan_structure()

    call_command("delete_orphan_structures", "--wet-run")

    assert not Structure.objects.filter(pk=structure.pk).exists()


def test_dry_run_deletes_nothing():
    structure = make_orphan_structure()

    call_command("delete_orphan_structures")

    assert Structure.objects.filter(pk=structure.pk).exists()


@pytest.mark.parametrize(
    "prepare",
    [
        pytest.param(
            lambda structure: make_structure_member(
                user=make_user(), structure=structure
            ),
            id="member",
        ),
        pytest.param(
            lambda structure: StructurePutativeMember(
                user=make_user(), structure=structure
            ).save(),
            id="putative-member",
        ),
        pytest.param(
            lambda structure: make_service(structure=structure),
            id="service",
        ),
        pytest.param(
            lambda structure: Structure.objects.filter(pk=structure.pk).update(
                admin_already_invited=True
            ),
            id="admin-already-invited",
        ),
        pytest.param(
            lambda structure: make_structure(parent=structure, siret=None),
            id="parent-structure",
        ),
        pytest.param(
            lambda structure: baker.make(
                "services.AccessCondition", structure=structure
            ),
            id="custom-access-condition",
        ),
        pytest.param(
            lambda structure: baker.make("services.Requirement", structure=structure),
            id="custom-requirement",
        ),
        pytest.param(
            lambda structure: baker.make("services.Credential", structure=structure),
            id="custom-credential",
        ),
    ],
)
def test_preserves_structures(prepare):
    structure = make_orphan_structure()
    prepare(structure)

    call_command("delete_orphan_structures", "--wet-run")

    assert Structure.objects.filter(pk=structure.pk).exists()


def test_preserves_recent_structure():
    structure = make_orphan_structure(created_at=CREATED_BEFORE + timedelta(days=1))

    call_command("delete_orphan_structures", "--wet-run")

    assert Structure.objects.filter(pk=structure.pk).exists()


def test_deletes_related_objects():
    structure = make_orphan_structure()
    kept_structure = make_structure(user=make_user())

    label = baker.make("structures.StructureNationalLabel")
    structure.national_labels.add(label)

    log_item = baker.make("core.LogItem", structure=structure)
    kept_log_item = baker.make("core.LogItem", structure=kept_structure)

    call_command("delete_orphan_structures", "--wet-run")

    assert not LogItem.objects.filter(pk=log_item.pk).exists()
    assert LogItem.objects.filter(pk=kept_log_item.pk).exists()

    # seule l'association au label national disparait, pas le label lui-même
    assert not Structure.national_labels.through.objects.filter(
        structure_id=structure.pk
    ).exists()
    assert StructureNationalLabel.objects.filter(pk=label.pk).exists()


def test_deletes_orphan_branch():
    structure = make_structure(user=make_user())
    branch = make_orphan_structure(parent=structure, siret=None)

    call_command("delete_orphan_structures", "--wet-run")

    assert not Structure.objects.filter(pk=branch.pk).exists()
    assert Structure.objects.filter(pk=structure.pk).exists()
