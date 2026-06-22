import pytest

from dora.core.test_utils import (
    make_emplois_orientation,
    make_jwt_orientation,
    make_orientation,
)
from dora.orientations.models import PrescriberInfo

pytestmark = pytest.mark.django_db


def test_dora_orientation_uses_prescriber_account():
    orientation = make_orientation()

    assert orientation.prescriber_info == PrescriberInfo(
        full_name=orientation.prescriber.get_full_name(),
        first_name=orientation.prescriber.get_short_name(),
        email=orientation.prescriber.email,
        structure_name=orientation.prescriber_structure.name,
        structure_slug=orientation.prescriber_structure.slug,
        structure_url=orientation.prescriber_structure.get_frontend_url(),
    )


def test_emplois_orientation_uses_emplois_data():
    orientation = make_emplois_orientation()
    data = orientation.emplois_orientation_data

    assert orientation.prescriber_info == PrescriberInfo(
        full_name=f"{data.prescriber_first_name} {data.prescriber_last_name}",
        first_name=data.prescriber_first_name,
        email=data.prescriber_email,
        structure_name=data.structure_name,
        structure_slug="",
    )


def test_jwt_orientation_uses_prescriber_account():
    orientation = make_jwt_orientation()

    assert orientation.prescriber_info.full_name == (
        orientation.prescriber.get_full_name()
    )
    assert orientation.prescriber_info.email == orientation.prescriber.email


def test_deleted_prescriber_yields_empty_info():
    orientation = make_orientation(prescriber=None, prescriber_structure=None)

    assert orientation.prescriber_info == PrescriberInfo()


def test_deleted_prescriber_keeps_structure_info():
    orientation = make_orientation(prescriber=None)

    assert orientation.prescriber_info.full_name == ""
    assert orientation.prescriber_info.email == ""
    assert (
        orientation.prescriber_info.structure_name
        == orientation.prescriber_structure.name
    )
