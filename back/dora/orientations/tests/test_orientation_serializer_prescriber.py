import pytest

from dora.core.test_utils import (
    make_emplois_orientation,
    make_jwt_orientation,
    make_orientation,
)
from dora.orientations.serializers import OrientationSerializer

pytestmark = pytest.mark.django_db


def test_get_prescriber_uses_emplois_data_when_present():
    orientation = make_emplois_orientation(
        emplois_data={
            "prescriber_first_name": "Jean-Prescripteur",
            "prescriber_last_name": "des Emplois",
            "prescriber_email": "jean-prescripteur.des-emplois@example.com",
        }
    )

    prescriber = OrientationSerializer().get_prescriber(orientation)

    assert prescriber == {
        "name": "Jean-Prescripteur des Emplois",
        "email": "jean-prescripteur.des-emplois@example.com",
    }


def test_get_prescriber_structure_uses_emplois_data_when_present():
    orientation = make_emplois_orientation(
        emplois_data={
            "structure_name": "Structure des Emplois",
        }
    )

    prescriber_structure = OrientationSerializer().get_prescriber_structure(orientation)

    assert prescriber_structure == {
        "name": "Structure des Emplois",
        "slug": "",
        "url": None,
    }


def test_get_prescriber_falls_back_to_dora_prescriber():
    orientation = make_orientation()

    prescriber = OrientationSerializer().get_prescriber(orientation)

    assert prescriber == {
        "name": orientation.prescriber.get_full_name(),
        "email": orientation.prescriber.email,
    }


def test_get_prescriber_structure_falls_back_to_dora_structure():
    orientation = make_orientation()

    prescriber_structure = OrientationSerializer().get_prescriber_structure(orientation)

    assert prescriber_structure == {
        "name": orientation.prescriber_structure.name,
        "slug": orientation.prescriber_structure.slug,
        "url": orientation.prescriber_structure.get_frontend_url(),
    }


def test_get_prescriber_uses_dora_data_for_jwt_orientation():
    orientation = make_jwt_orientation()

    assert OrientationSerializer().get_prescriber(orientation) == {
        "name": orientation.prescriber.get_full_name(),
        "email": orientation.prescriber.email,
    }
    assert OrientationSerializer().get_prescriber_structure(orientation) == {
        "name": orientation.prescriber_structure.name,
        "slug": orientation.prescriber_structure.slug,
        "url": orientation.prescriber_structure.get_frontend_url(),
    }


def test_serialized_prescriber_matches_prescriber_info(orientation):
    prescriber = orientation.prescriber_info

    data = OrientationSerializer(orientation).data

    assert data["prescriber"] == {
        "name": prescriber.full_name,
        "email": prescriber.email,
    }
    assert data["prescriber_structure"] == {
        "name": prescriber.structure_name,
        "slug": prescriber.structure_slug,
        "url": prescriber.structure_url or None,
    }
