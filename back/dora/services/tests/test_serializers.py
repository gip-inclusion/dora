import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker

from dora.core.test_utils import make_published_service, make_service
from dora.services.models import Bookmark, Public, ServiceSource
from dora.services.serializers import BookmarkSerializer, SearchResultSerializer

TOUS_PUBLICS = DiPublic.TOUS_PUBLICS.value


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


def test_search_di_publics_empty_maps_to_tous():
    # Aucun public -> publics_di == [] -> réinterprété « tous-publics » à l'affichage.
    service = make_service()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == [TOUS_PUBLICS]


def test_search_di_publics_all_referential_maps_to_tous():
    # Tout le référentiel sélectionné se présente comme « tous-publics » (collapse à l'affichage,
    # la colonne reste fidèle).
    service = make_service()
    for public in DiPublic:
        if public.value != TOUS_PUBLICS:
            service.publics.add(
                baker.make(
                    Public, name=public.value, corresponding_di_publics=[public.value]
                )
            )
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == [TOUS_PUBLICS]


def test_search_di_publics_returns_specific_publics():
    service = make_service()
    service.publics.add(
        baker.make(
            Public, name="familles", corresponding_di_publics=[DiPublic.FAMILLES.value]
        ),
        baker.make(
            Public,
            name="etudiants",
            corresponding_di_publics=[DiPublic.ETUDIANTS.value],
        ),
    )
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == sorted(
        [DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value]
    )
