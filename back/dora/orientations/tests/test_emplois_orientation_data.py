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
