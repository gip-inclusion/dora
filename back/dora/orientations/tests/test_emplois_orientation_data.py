from uuid import uuid4

import pytest

from dora.orientations.models import EmploisOrientationData


@pytest.mark.parametrize(
    "first_name,last_name,email,expected",
    [
        (
            "Jean-Prescripteur",
            "des Emplois",
            "jean-prescripteur.des-emplois@example.com",
            "Jean-Prescripteur des Emplois",
        ),
        ("Jean", "", "jean@example.com", "Jean"),
        ("", "Prescripteur", "prescripteur@example.com", "Prescripteur"),
        ("", "", "jp@example.com", "jp@example.com"),
    ],
)
def test_emplois_orientation_data_prescriber_full_name(
    first_name, last_name, email, expected
):
    data = EmploisOrientationData(
        prescriber_first_name=first_name,
        prescriber_last_name=last_name,
        prescriber_email=email,
    )
    assert data.prescriber_full_name == expected


@pytest.mark.parametrize(
    "base_url",
    [
        "https://emplois.inclusion.beta.gouv.fr",
        "https://emplois.inclusion.beta.gouv.fr/",
    ],
)
def test_emplois_orientation_data_structure_url(settings, base_url):
    settings.EMPLOIS_FRONTEND_URL = base_url
    structure_id = uuid4()
    data = EmploisOrientationData(structure_id=structure_id)
    assert (
        data.structure_url
        == f"https://emplois.inclusion.beta.gouv.fr/insertion/structure/{structure_id}/card"
    )
