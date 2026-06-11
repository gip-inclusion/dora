from uuid import uuid4

import pytest

from dora.core.test_utils import make_emplois_orientation, make_orientation
from dora.orientations.models import EmploisOrientationData, PrescriberInfo

pytestmark = pytest.mark.django_db


def test_prescriber_info_dora_orientation():
    orientation = make_orientation()

    assert orientation.prescriber_info == PrescriberInfo(
        full_name=orientation.prescriber.get_full_name(),
        email=orientation.prescriber.email,
        structure_name=orientation.prescriber_structure.name,
        structure_url=orientation.prescriber_structure.get_frontend_url(),
    )


def test_prescriber_info_emplois_orientation(settings):
    settings.EMPLOIS_FRONTEND_URL = "https://emplois.inclusion.beta.gouv.fr"
    orientation = make_emplois_orientation()

    assert orientation.prescriber_info == PrescriberInfo(
        full_name=orientation.emplois_orientation_data.prescriber_full_name,
        email=orientation.emplois_orientation_data.prescriber_email,
        structure_name=orientation.emplois_orientation_data.structure_name,
        structure_url=orientation.emplois_orientation_data.structure_url,
    )


def test_prescriber_info_jwt_orientation_prefers_dora_data():
    # Flux JWT : prescripteur + structure Dora ET des données Les Emplois
    # partielles (beneficiary_id / structure_id seulement). Les données Dora
    # priment sur les champs Emplois vides.
    orientation = make_orientation()
    EmploisOrientationData.objects.create(
        orientation=orientation, beneficiary_id=uuid4(), structure_id=uuid4()
    )

    assert orientation.prescriber_info == PrescriberInfo(
        full_name=orientation.prescriber.get_full_name(),
        email=orientation.prescriber.email,
        structure_name=orientation.prescriber_structure.name,
        structure_url=orientation.prescriber_structure.get_frontend_url(),
    )


def test_prescriber_info_deleted_prescriber_keeps_structure():
    orientation = make_orientation(prescriber=None)

    assert orientation.prescriber_info == PrescriberInfo(
        full_name="",
        email="",
        structure_name=orientation.prescriber_structure.name,
        structure_url=orientation.prescriber_structure.get_frontend_url(),
    )


def test_prescriber_info_without_any_source_is_empty():
    orientation = make_orientation(prescriber=None, prescriber_structure=None)

    assert orientation.prescriber_info == PrescriberInfo("", "", "", "")
