import pytest
from data_inclusion.schema.v1 import ModeMobilisation
from data_inclusion.schema.v1.publics import Public as DiPublic
from model_bakery import baker
from rest_framework.test import APIRequestFactory, force_authenticate

from dora.core.test_utils import (
    make_model,
    make_published_service,
    make_service,
    make_structure,
)
from dora.services.models import Bookmark, CoachOrientationMode, ServiceSource
from dora.services.serializers import (
    DORA_FORM,
    MOBILISATION_LINK_MODE,
    BookmarkSerializer,
    SearchResultSerializer,
    ServiceModelSerializer,
    ServiceSerializer,
)
from dora.services.utils import DI_PUBLICS_ORDER, update_sync_checksum

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


def serialize_dora_form_write(service, user, data):
    # Passe par la validation complète du sérialiseur : c'est elle qui arbitre entre
    # `coach_orientation_modes` (préférence v1) et `mobilisation_modes` (contrat DI).
    request = APIRequestFactory().patch(f"/services/{service.slug}/")
    force_authenticate(request, user=user)
    request.user = user

    return ServiceSerializer(
        instance=service,
        data=data,
        partial=True,
        context={"request": request},
    )


@pytest.fixture
def editable_service():
    user = baker.make("users.User", is_valid=True)
    return make_service(structure=make_structure(user)), user


def test_dora_form_write_strips_mobilisation_link_mode(editable_service):
    # data·inclusion rejette `utiliser-lien-mobilisation` sans `lien_mobilisation` :
    # la préférence est enregistrée en v1, la colonne v2 reste publiable.
    service, user = editable_service
    serializer = serialize_dora_form_write(
        service,
        user,
        {
            "coach_orientation_modes": [DORA_FORM],
            "mobilisation_modes": [MOBILISATION_LINK_MODE, "telephoner"],
            "mobilisation_link": None,
        },
    )

    assert serializer.is_valid(), serializer.errors
    assert serializer.validated_data["mobilisation_modes"] == ["telephoner"]
    assert serializer.validated_data["mobilisation_link"] is None

    service = serializer.save()
    assert service.mobilisation_modes == ["telephoner"]
    assert [m.value for m in service.coach_orientation_modes.all()] == [DORA_FORM]


def test_custom_link_write_keeps_mobilisation_link_mode(editable_service):
    service, user = editable_service
    serializer = serialize_dora_form_write(
        service,
        user,
        {
            "coach_orientation_modes": [],
            "mobilisation_modes": [MOBILISATION_LINK_MODE],
            "mobilisation_link": "https://exemple.fr/mon-formulaire",
        },
    )

    assert serializer.is_valid(), serializer.errors
    service = serializer.save()
    assert service.mobilisation_modes == [MOBILISATION_LINK_MODE]
    assert service.mobilisation_link == "https://exemple.fr/mon-formulaire"
    assert not service.coach_orientation_modes.exists()


def test_mobilisation_link_mode_without_link_nor_dora_form_is_rejected(
    editable_service,
):
    # Cas d'une structure sans formulaire Dora : « votre propre formulaire » est le
    # seul choix possible, donc un lien vide ne peut être qu'une saisie manquante.
    service, user = editable_service
    serializer = serialize_dora_form_write(
        service,
        user,
        {
            "coach_orientation_modes": [],
            "mobilisation_modes": [MOBILISATION_LINK_MODE],
            "mobilisation_link": None,
        },
    )

    assert not serializer.is_valid()
    assert "mobilisation_link" in serializer.errors


def test_dora_form_representation_reinjects_mobilisation_link_mode(editable_service):
    # Le mode n'est pas stocké : il est réinjecté à la lecture pour que la case soit
    # cochée dans le formulaire d'édition.
    service, user = editable_service
    service.mobilisation_modes = ["telephoner"]
    service.save()
    service.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value=DORA_FORM)
    )

    request = APIRequestFactory().get(f"/services/{service.slug}/")
    force_authenticate(request, user=user)
    request.user = user
    data = ServiceSerializer(instance=service, context={"request": request}).data

    assert data["mobilisation_modes"] == ["telephoner", MOBILISATION_LINK_MODE]
    assert (
        ModeMobilisation(MOBILISATION_LINK_MODE).label
        in data["mobilisation_modes_display"]
    )
    # La colonne, elle, reste publiable pour data·inclusion.
    service.refresh_from_db()
    assert service.mobilisation_modes == ["telephoner"]


def test_representation_untouched_without_dora_form(editable_service):
    service, user = editable_service
    service.mobilisation_modes = ["telephoner"]
    service.save()

    request = APIRequestFactory().get(f"/services/{service.slug}/")
    force_authenticate(request, user=user)
    request.user = user
    data = ServiceSerializer(instance=service, context={"request": request}).data

    assert data["mobilisation_modes"] == ["telephoner"]


def test_dora_form_representation_leaves_sync_checksum_untouched():
    # `coach_orientation_modes` est haché par `update_sync_checksum`
    # (`SYNC_M2M_FIELDS`) : la réinjection ne doit vivre que dans la représentation,
    # sous peine de faire basculer toutes les copies d'un modèle en « modèle modifié ».
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    model = make_model(structure=structure)
    model.mobilisation_modes = ["telephoner"]
    model.save()
    model.coach_orientation_modes.set(
        CoachOrientationMode.objects.filter(value=DORA_FORM)
    )

    checksum_before = update_sync_checksum(model)

    request = APIRequestFactory().get(f"/models/{model.slug}/")
    force_authenticate(request, user=user)
    request.user = user
    data = ServiceModelSerializer(instance=model, context={"request": request}).data

    assert data["mobilisation_modes"] == ["telephoner", MOBILISATION_LINK_MODE]

    model.refresh_from_db()
    assert update_sync_checksum(model) == checksum_before


def test_dora_form_write_leaves_sync_checksum_untouched():
    # Même garantie à l'écriture : enregistrer un modèle « formulaire Dora » ne doit pas
    # bouger l'empreinte entre l'instance en mémoire et celle relue en base.
    user = baker.make("users.User", is_valid=True)
    structure = make_structure(user)
    model = make_model(structure=structure)

    request = APIRequestFactory().patch(f"/models/{model.slug}/")
    force_authenticate(request, user=user)
    request.user = user
    serializer = ServiceModelSerializer(
        instance=model,
        data={
            "coach_orientation_modes": [DORA_FORM],
            "mobilisation_modes": [MOBILISATION_LINK_MODE, "telephoner"],
            "mobilisation_link": None,
        },
        partial=True,
        context={"request": request},
    )
    assert serializer.is_valid(), serializer.errors
    saved = serializer.save()

    in_memory = update_sync_checksum(saved)
    saved.refresh_from_db()
    assert update_sync_checksum(saved) == in_memory
