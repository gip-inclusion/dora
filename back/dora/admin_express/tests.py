import pytest
from django.contrib.gis.geos import MultiPolygon, Polygon

from dora.admin_express.models import Department


@pytest.fixture
def test_department():
    """Fixture pour créer un département de test avec une géométrie simple."""
    # Création d'un polygone simple (carré)
    polygon = Polygon(
        (
            (2.224121, 48.902459),  # Premier point
            (2.224121, 48.912459),  # Deuxième point
            (2.234121, 48.912459),  # Troisième point
            (2.234121, 48.902459),  # Quatrième point
            (2.224121, 48.902459),  # Point de fermeture (identique au premier)
        )
    )
    # Création d'un MultiPolygon à partir du polygone
    multipolygon = MultiPolygon(polygon)

    return Department.objects.create(
        code="75",
        name="Paris",
        normalized_name="paris",
        region="11",
        geom=multipolygon,
    )
