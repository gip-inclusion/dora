from uuid import uuid4

import pytest

from dora.core.test_utils import make_emplois_orientation, make_orientation
from dora.orientations.models import EmploisOrientationData
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


def test_get_prescriber_structure_uses_emplois_data_when_present(settings):
    settings.EMPLOIS_FRONTEND_URL = "https://emplois.inclusion.beta.gouv.fr"
    orientation = make_emplois_orientation(
        emplois_data={"structure_name": "Structure des Emplois"}
    )
    structure_id = orientation.emplois_orientation_data.structure_id

    prescriber_structure = OrientationSerializer().get_prescriber_structure(orientation)

    assert prescriber_structure == {
        "name": "Structure des Emplois",
        "url": f"https://emplois.inclusion.beta.gouv.fr/insertion/structure/{structure_id}/card",
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
        "url": orientation.prescriber_structure.get_frontend_url(),
    }


def test_get_prescriber_uses_dora_data_for_jwt_orientation():
    # Flux JWT : prescripteur + structure Dora ET emplois_orientation_data
    # (avec seulement beneficiary_id et structure_id). On doit afficher
    # le prescripteur Dora, pas les champs Emplois vides.
    orientation = make_orientation()
    EmploisOrientationData.objects.create(
        orientation=orientation, beneficiary_id=uuid4(), structure_id=uuid4()
    )
    orientation.refresh_from_db()

    assert OrientationSerializer().get_prescriber(orientation) == {
        "name": orientation.prescriber.get_full_name(),
        "email": orientation.prescriber.email,
    }
    assert OrientationSerializer().get_prescriber_structure(orientation) == {
        "name": orientation.prescriber_structure.name,
        "url": orientation.prescriber_structure.get_frontend_url(),
    }
