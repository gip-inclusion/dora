import pytest

from dora.core.test_utils import make_published_service
from dora.services.models import Bookmark, ServiceSource
from dora.services.serializers import BookmarkSerializer


@pytest.fixture
def service_with_source():
    ServiceSource(label="a-random-source").save()
    assert ServiceSource.objects.count() > 0
    return make_published_service(source=ServiceSource.objects.first())


def test_service_bookmark_serialization(service_with_source):
    bookmark = Bookmark(service=service_with_source)
    data = BookmarkSerializer(bookmark).data

    # Teste la sérialisation correcte de la source du service
    assert data["service"]["source"] == service_with_source.source.label
