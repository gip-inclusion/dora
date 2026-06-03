import uuid

import pytest
from django.urls import reverse
from model_bakery import baker

from dora.core.test_utils import make_published_service, make_structure
from dora.stats.models import DiMobilisationEvent, MobilisationEvent, StructureInfosView

URL = reverse("emplois:mobilisation-event")


@pytest.fixture
def base_payload():
    return {
        "anonymous_user_hash": "a" * 32,
        "user_kind": "emplois_prescripteur",
        "structure_id": "dora--ma-structure",
        "source": "dora",
    }


# ─── Auth / Permissions ───────────────────────────────────────────────────────


def test_requires_authentication(api_client, base_payload):
    assert api_client.post(URL, data=base_payload).status_code == 401


def test_requires_emplois_email(api_client, base_payload):
    other_user = baker.make("users.User", is_valid=True, email="other@example.com")
    api_client.force_authenticate(user=other_user)
    assert api_client.post(URL, data=base_payload).status_code == 403


@pytest.mark.parametrize("method", ["get", "patch", "delete"])
def test_post_only(emplois_api_client, method):
    # La permission OrientationAPIPermission rejette les méthodes non-POST avant
    # que Django puisse retourner un 405.
    assert getattr(emplois_api_client, method)(URL).status_code == 403


# ─── Validation ───────────────────────────────────────────────────────────────


@pytest.mark.parametrize(
    "invalid_hash",
    ["abc", "x" * 32, "a" * 31, "a" * 33, ""],
    ids=["too_short", "non_hex", "31_chars", "33_chars", "empty"],
)
def test_invalid_anonymous_user_hash(
    emplois_api_client, base_payload, invalid_hash
):
    base_payload["anonymous_user_hash"] = invalid_hash
    assert emplois_api_client.post(URL, data=base_payload).status_code == 400


def test_invalid_user_kind(emplois_api_client, base_payload):
    base_payload["user_kind"] = "accompagnateur"
    assert emplois_api_client.post(URL, data=base_payload).status_code == 400


@pytest.mark.parametrize(
    "missing_field",
    ["anonymous_user_hash", "user_kind", "structure_id", "source"],
)
def test_missing_required_field(emplois_api_client, base_payload, missing_field):
    del base_payload[missing_field]
    assert emplois_api_client.post(URL, data=base_payload).status_code == 400


# ─── StructureInfosView (pas de service_id, source Dora) ──────────────────────


def test_creates_structure_infos_view(emplois_api_client, base_payload):
    structure = make_structure(city_code="75056")
    base_payload["structure_id"] = f"dora--{structure.pk}"

    response = emplois_api_client.post(URL, data=base_payload)

    assert response.status_code == 201
    event = StructureInfosView.objects.get()
    assert event.anonymous_user_hash == "a" * 32
    assert event.user_kind == "emplois_prescripteur"
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


@pytest.mark.parametrize(
    "structure_id",
    [f"dora--{uuid.uuid4()}", "dora--not-a-uuid"],
    ids=["unknown_uuid", "invalid_uuid"],
)
def test_returns_404_when_dora_structure_not_found(
    emplois_api_client, base_payload, structure_id
):
    base_payload["structure_id"] = structure_id

    response = emplois_api_client.post(URL, data=base_payload)

    assert response.status_code == 404
    assert response.data["detail"]["code"] == "not_found"
    assert str(response.data["detail"]["message"]) == (
        "Structure Dora introuvable pour cet identifiant."
    )
    assert StructureInfosView.objects.count() == 0


def test_ignores_non_dora_structure(emplois_api_client, base_payload):
    # Il n'existe pas de structure non-Dora sur Dora : rien n'est enregistré.
    base_payload["source"] = "soliguide"
    base_payload["structure_id"] = "soliguide--ma-structure"

    response = emplois_api_client.post(URL, data=base_payload)

    assert response.status_code == 204
    assert StructureInfosView.objects.count() == 0


# ─── MobilisationEvent (service Dora) ─────────────────────────────────────────


def test_creates_mobilisation_event_for_dora_service(
    emplois_api_client, base_payload
):
    service = make_published_service()
    service.structure.city_code = "69123"
    service.structure.save()
    base_payload["service_id"] = f"dora--{service.pk}"
    base_payload["structure_id"] = f"dora--{service.structure.pk}"
    base_payload["external_link"] = "https://example.org/offre"

    response = emplois_api_client.post(URL, data=base_payload)

    assert response.status_code == 201
    event = MobilisationEvent.objects.get()
    assert event.anonymous_user_hash == "a" * 32
    assert event.user_kind == "emplois_prescripteur"
    assert event.service == service
    assert event.structure == service.structure
    assert event.structure_department == "69"
    assert event.structure_city_code == "69123"
    assert event.external_link == "https://example.org/offre"
    assert event.path == ""
    assert event.user is None
    assert event.is_logged is False
    assert event.is_staff is False
    assert event.is_manager is False
    assert event.is_an_admin is False
    assert event.is_structure_member is False
    assert event.is_structure_admin is False


@pytest.mark.parametrize(
    "service_id",
    [f"dora--{uuid.uuid4()}", "dora--not-a-uuid"],
    ids=["unknown_uuid", "invalid_uuid"],
)
def test_returns_404_when_dora_service_not_found(
    emplois_api_client, base_payload, service_id
):
    base_payload["service_id"] = service_id

    response = emplois_api_client.post(URL, data=base_payload)

    assert response.status_code == 404
    assert response.data["detail"]["code"] == "not_found"
    assert str(response.data["detail"]["message"]) == (
        "Service Dora introuvable pour cet identifiant."
    )
    assert MobilisationEvent.objects.count() == 0


# ─── DiMobilisationEvent (service hors Dora) ──────────────────────────────────


def test_creates_di_mobilisation_event(emplois_api_client):
    response = emplois_api_client.post(
        URL,
        data={
            "anonymous_user_hash": "a" * 32,
            "user_kind": "emplois_prescripteur",
            "service_id": "soliguide--abc123",
            "structure_id": "soliguide--struct-xyz",
            "source": "soliguide",
            "service_name": "Accueil et orientation",
            "structure_name": "CCAS Paris",
            "structure_department": "75",
        },
    )

    assert response.status_code == 201
    event = DiMobilisationEvent.objects.get()
    assert event.anonymous_user_hash == "a" * 32
    assert event.user_kind == "emplois_prescripteur"
    assert event.service_id == "soliguide--abc123"
    assert event.structure_id == "soliguide--struct-xyz"
    assert event.source == "soliguide"
    assert event.service_name == "Accueil et orientation"
    assert event.structure_name == "CCAS Paris"
    assert event.structure_department == "75"
    assert event.path == ""
    assert event.user is None
    assert event.is_logged is False
    assert event.is_staff is False
    assert event.is_manager is False
    assert event.is_an_admin is False
    assert event.external_link is None


@pytest.mark.parametrize(
    "missing_field",
    ["service_name", "structure_name", "structure_department"],
)
def test_non_dora_service_requires_metadata(emplois_api_client, missing_field):
    payload = {
        "anonymous_user_hash": "a" * 32,
        "user_kind": "emplois_prescripteur",
        "service_id": "soliguide--abc123",
        "structure_id": "soliguide--struct-xyz",
        "source": "soliguide",
        "service_name": "Accueil",
        "structure_name": "CCAS",
        "structure_department": "75",
    }
    del payload[missing_field]

    response = emplois_api_client.post(URL, data=payload)

    assert response.status_code == 400
    assert missing_field in response.data
    assert DiMobilisationEvent.objects.count() == 0
