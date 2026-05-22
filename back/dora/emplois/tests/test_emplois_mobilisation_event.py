import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_published_service, make_structure
from dora.stats.models import DiMobilisationEvent, MobilisationEvent, StructureInfosView

URL = reverse("emplois:mobilisation-event")
VALID_HASH = "a" * 32


def post_event(api_client, data):
    return api_client.post(URL, data=data)


@pytest.fixture
def base_payload():
    return {
        "anonymous_user_hash": VALID_HASH,
        "user_kind": "emplois_accompagnateur",
        "structure_id": "dora--ma-structure",
        "source": "dora",
    }


# ─── Auth / Permissions ───────────────────────────────────────────────────────


def test_requires_authentication(api_client, base_payload):
    assert post_event(api_client, base_payload).status_code == 401


def test_requires_emplois_email(api_client, base_payload):
    other_user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=other_user)
    assert post_event(api_client, base_payload).status_code == 403


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_post_only(emplois_user, api_client, method):
    # La permission OrientationAPIPermission rejette les méthodes non-POST avant
    # que Django puisse retourner un 405.
    assert getattr(api_client, method)(URL).status_code == 403


# ─── Validation ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "invalid_hash",
    ["abc", "x" * 32, "a" * 31, "a" * 33, ""],
    ids=["too_short", "non_hex", "31_chars", "33_chars", "empty"],
)
def test_invalid_anonymous_user_hash(
    emplois_user, api_client, base_payload, invalid_hash
):
    base_payload["anonymous_user_hash"] = invalid_hash
    assert post_event(api_client, base_payload).status_code == 400


def test_invalid_user_kind(emplois_user, api_client, base_payload):
    base_payload["user_kind"] = "accompagnateur"
    assert post_event(api_client, base_payload).status_code == 400


@pytest.mark.parametrize(
    "missing_field",
    ["anonymous_user_hash", "user_kind", "structure_id", "source"],
)
def test_missing_required_field(emplois_user, api_client, base_payload, missing_field):
    del base_payload[missing_field]
    assert post_event(api_client, base_payload).status_code == 400


# ─── StructureInfosView ───────────────────────────────────────────────────────


def test_creates_structure_infos_view(emplois_user, api_client, base_payload):
    structure = make_structure(city_code="75056")
    base_payload["structure_id"] = f"dora--{structure.pk}"

    response = post_event(api_client, base_payload)

    assert response.status_code == 201
    event = StructureInfosView.objects.get()
    assert event.anonymous_user_hash == VALID_HASH
    assert event.user_kind == "emplois_accompagnateur"
    assert event.structure == structure
    assert event.structure_department == "75"
    assert event.structure_city_code == "75056"
    assert event.path == ""
    assert event.user is None
    assert event.is_logged is False
    assert event.is_staff is False
    assert event.is_manager is False
    assert event.is_an_admin is False
    assert event.is_structure_member is False
    assert event.is_structure_admin is False


def test_creates_structure_infos_view_when_structure_not_found(
    emplois_user, api_client, base_payload
):
    base_payload["structure_id"] = "dora--00000000-0000-0000-0000-000000000000"

    response = post_event(api_client, base_payload)

    assert response.status_code == 201
    event = StructureInfosView.objects.get()
    assert event.structure is None
    assert event.structure_department == ""
    assert event.structure_city_code == ""


def test_returns_204_when_service_id_empty_and_non_dora_source(
    emplois_user, api_client, base_payload
):
    base_payload["source"] = "soliguide"
    base_payload["structure_id"] = "soliguide--ma-structure"

    response = post_event(api_client, base_payload)

    assert response.status_code == 204
    assert StructureInfosView.objects.count() == 0


# ─── MobilisationEvent ────────────────────────────────────────────────────────


def test_creates_mobilisation_event_for_dora_service(
    emplois_user, api_client, base_payload
):
    service = make_published_service()
    service.structure.city_code = "69123"
    service.structure.save()
    base_payload["service_id"] = f"dora--{service.pk}"
    base_payload["structure_id"] = f"dora--{service.structure.pk}"

    response = post_event(api_client, base_payload)

    assert response.status_code == 201
    event = MobilisationEvent.objects.get()
    assert event.anonymous_user_hash == VALID_HASH
    assert event.user_kind == "emplois_accompagnateur"
    assert event.service == service
    assert event.structure == service.structure
    assert event.structure_department == "69"
    assert event.structure_city_code == "69123"
    assert event.path == ""
    assert event.user is None
    assert event.is_logged is False
    assert event.is_staff is False
    assert event.is_manager is False
    assert event.is_an_admin is False
    assert event.is_structure_member is False
    assert event.is_structure_admin is False
    assert event.external_link is None


# ─── DiMobilisationEvent ─────────────────────────────────────────────────────


def test_creates_di_mobilisation_event(emplois_user, api_client):
    response = post_event(
        api_client,
        {
            "anonymous_user_hash": VALID_HASH,
            "user_kind": "emplois_accompagnateur",
            "service_id": "soliguide--abc123",
            "structure_id": "soliguide--struct-xyz",
            "source": "soliguide",
        },
    )

    assert response.status_code == 201
    event = DiMobilisationEvent.objects.get()
    assert event.anonymous_user_hash == VALID_HASH
    assert event.user_kind == "emplois_accompagnateur"
    assert event.service_id == "soliguide--abc123"
    assert event.structure_id == "soliguide--struct-xyz"
    assert event.source == "soliguide"
    assert event.service_name == ""
    assert event.structure_name == ""
    assert event.structure_department == ""
    assert event.path == ""
    assert event.user is None
    assert event.is_logged is False
    assert event.is_staff is False
    assert event.is_manager is False
    assert event.is_an_admin is False
    assert event.external_link is None
