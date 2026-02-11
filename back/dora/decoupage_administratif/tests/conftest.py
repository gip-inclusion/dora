import pytest
from django.contrib.gis.geos import Point

from dora.core.constants import WGS84
from dora.decoupage_administratif.models import City


@pytest.fixture
def test_cities(db):
    """Fixture pour créer les villes de test communes."""
    City.objects.create(
        code="75056",
        name="Paris",
        department="75",
        region="11",
        epci="200055781",
        normalized_name="PARIS",
        center=Point(2.3522, 48.8566, srid=WGS84),
    )
    City.objects.create(
        code="69123",
        name="Lyon",
        department="69",
        region="84",
        epci="200046977",
        normalized_name="LYON",
        center=Point(4.8357, 45.7640, srid=WGS84),
    )
    City.objects.create(
        code="2A004",
        name="Ajaccio",
        department="2A",
        region="94",
        epci="200040947",
        normalized_name="AJACCIO",
        center=Point(8.7386, 41.9258, srid=WGS84),
    )
