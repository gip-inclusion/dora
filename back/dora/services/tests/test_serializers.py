import pytest
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate

from dora.core.test_utils import make_published_service, make_service, make_structure
from dora.services.models import Bookmark, ServiceSource
from dora.services.serializers import (
    BookmarkSerializer,
    SearchResultSerializer,
    ServiceSerializer,
)
from dora.services.utils import DI_PUBLICS_ORDER

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
    # Aucun public -> publics == [] : « aucune restriction ». La lecture applicative
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
    service.publics = expected
    service.save()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == expected


def test_search_di_publics_returns_specific_publics():
    # Les publics sont portés directement par la colonne `publics`.
    service = make_service()
    service.publics = sorted([DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value])
    service.save()
    service.refresh_from_db()
    assert SearchResultSerializer().get_di_publics(service) == sorted(
        [DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value]
    )


def validate_publics(publics):
    # `ServiceSerializer.validate` normalise `publics` : on passe par la validation
    # complète du sérialiseur pour vérifier ce que l'écriture persistera réellement.
    user = baker.make("users.User", is_valid=True)
    service = make_service(structure=make_structure(user))

    request = APIRequestFactory().patch(f"/services/{service.slug}/")
    force_authenticate(request, user=user)
    request.user = user

    serializer = ServiceSerializer(
        instance=service,
        data={"publics": publics},
        partial=True,
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    return serializer.validated_data["publics"]


def test_validate_publics_deduplicates():
    assert validate_publics(
        [DiPublic.FAMILLES.value, DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value]
    ) == sorted(
        [DiPublic.FAMILLES.value, DiPublic.ETUDIANTS.value],
        key=DI_PUBLICS_ORDER.__getitem__,
    )


def test_validate_publics_is_order_independent():
    # Deux saisies équivalentes doivent donner la même liste : c'est ce qui garantit que
    # l'empreinte de synchronisation, l'historique et le diff « modèle modifié » ne
    # réagissent pas à un simple réordonnancement.
    publics = [
        DiPublic.FAMILLES.value,
        DiPublic.ETUDIANTS.value,
        DiPublic.JEUNES.value,
    ]
    assert validate_publics(publics) == validate_publics(list(reversed(publics)))


def test_validate_publics_follows_referential_order():
    # L'ordre de rangement est celui du référentiel DI, pas l'ordre alphabétique, pour
    # rester aligné sur l'affichage des libellés (`get_publics_display`).
    publics = [p.value for p in DiPublic if p.value != TOUS_PUBLICS]
    validated = validate_publics(list(reversed(publics)))

    assert validated == publics
    assert validated == sorted(publics, key=DI_PUBLICS_ORDER.__getitem__)
