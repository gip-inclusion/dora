import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic

from dora.core.test_utils import make_published_service, make_service
from dora.services.models import Bookmark, ServiceSource
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


def test_search_di_publics_empty_returns_empty():
    # Aucun public -> publics_di == [] : « aucune restriction ». La lecture applicative
    # n'inflate plus en `tous-publics` (réservé à l'interface DI) ; le front affiche
    # « Tous publics » sur la liste vide.
    service = make_service()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == []


def test_search_di_publics_all_referential_returned_as_is():
    # Le collapse « tout le référentiel -> tous-publics » n'a plus lieu en lecture
    # applicative : la colonne est renvoyée fidèlement.
    expected = sorted(p.value for p in DiPublic if p.value != TOUS_PUBLICS)
    service = make_service()
    service.publics_di = expected
    service.save()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == expected


def test_search_di_publics_returns_specific_publics():
    # Bascule d'écriture : les publics sont portés directement par la colonne `publics_di`.
    service = make_service()
    service.publics_di = sorted([DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value])
    service.save()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == sorted(
        [DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value]
    )
