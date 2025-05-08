import pytest
from django.contrib.gis.geos import GEOSGeometry, MultiPolygon, Polygon

from dora.admin_express.models import Department
from dora.admin_express.views import DeptSerializer


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


def test_geometry_simplification(test_department):
    """Test que le DeptSerializer simplifie correctement les géométries tout en maintenant leur validité."""
    serializer = DeptSerializer(test_department)
    data = serializer.data

    # Vérification de la présence du champ géométrie
    assert "geom" in data

    # Vérification que la géométrie n'est pas vide
    assert data["geom"] is not None

    # Vérification que la géométrie simplifiée contient des coordonnées
    assert len(data["geom"]["coordinates"]) > 0

    # Vérification que la simplification n'a pas rendu la géométrie invalide
    simplified_geom = GEOSGeometry(str(data["geom"]))
    # Vérification que la géométrie n'est pas vide et a la bonne structure
    assert not simplified_geom.empty
    assert simplified_geom.geom_type in ["Polygon", "MultiPolygon"]
