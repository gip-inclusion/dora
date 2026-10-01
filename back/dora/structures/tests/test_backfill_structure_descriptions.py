from django.core.management import call_command

from dora.core.test_utils import make_structure

SHORT_DESC = "Accompagnement vers l'emploi des jeunes de moins de vingt-six ans."
DESCRIPTION = "Ateliers collectifs de rédaction de CV et simulations d'entretien."


def test_copies_short_desc_into_empty_description():
    structure = make_structure(short_desc=SHORT_DESC, description="")

    call_command("backfill_structure_descriptions", "--wet-run")

    structure.refresh_from_db()
    assert structure.description == SHORT_DESC


def test_prepends_short_desc_to_description():
    structure = make_structure(short_desc=SHORT_DESC, description=DESCRIPTION)

    call_command("backfill_structure_descriptions", "--wet-run")

    structure.refresh_from_db()
    assert structure.description.startswith(SHORT_DESC)
    assert structure.description.endswith(DESCRIPTION)


def test_drops_short_desc_repeated_in_description():
    structure = make_structure(
        short_desc=SHORT_DESC, description=f"{SHORT_DESC}\n\n{DESCRIPTION}"
    )

    call_command("backfill_structure_descriptions", "--wet-run")

    structure.refresh_from_db()
    assert structure.description == f"{SHORT_DESC}\n\n{DESCRIPTION}"


def test_keeps_description_without_short_desc():
    structure = make_structure(short_desc="", description=DESCRIPTION)

    call_command("backfill_structure_descriptions", "--wet-run")

    structure.refresh_from_db()
    assert structure.description == DESCRIPTION


def test_dry_run_writes_nothing():
    structure = make_structure(short_desc=SHORT_DESC, description="")

    call_command("backfill_structure_descriptions")

    structure.refresh_from_db()
    assert structure.description == ""
