from datetime import timedelta

from django.utils import timezone
from model_bakery import baker

from dora.core.test_utils import make_model, make_structure
from dora.services.models import ServiceModificationHistoryItem


def test_editing_log_change(api_client):
    # fixture locale ?
    assert not ServiceModificationHistoryItem.objects.exists()

    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.patch(f"/models/{model.slug}/", {"name": "xxx"})

    assert 200 == response.status_code
    assert ServiceModificationHistoryItem.objects.exists()

    hitem = ServiceModificationHistoryItem.objects.first()

    assert hitem.user == user
    assert hitem.service == model
    assert hitem.fields == ["name"]
    assert timezone.now() - hitem.date < timedelta(seconds=1)


def test_editing_log_multiple_change(api_client):
    assert not ServiceModificationHistoryItem.objects.exists()

    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)
    api_client.force_authenticate(user=user)
    api_client.patch(f"/models/{model.slug}/", {"name": "xxx", "short_desc": "yyy"})
    hitem = ServiceModificationHistoryItem.objects.first()

    assert hitem.fields == ["name", "short_desc"]


def test_editing_log_m2m_change(api_client):
    assert not ServiceModificationHistoryItem.objects.exists()

    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)
    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/models/{model.slug}/", {"access_conditions": ["xxx"]}
    )

    assert 200 == response.status_code

    hitem = ServiceModificationHistoryItem.objects.first()

    assert hitem.fields == ["access_conditions"]


def test_editing_doesnt_log_current_status(api_client):
    assert not ServiceModificationHistoryItem.objects.exists()

    user = baker.make("users.User", is_valid=True)
    struct = make_structure(user)
    model = make_model(structure=struct)

    assert not ServiceModificationHistoryItem.objects.exists()

    api_client.force_authenticate(user=user)
    response = api_client.patch(
        f"/models/{model.slug}/", {"name": "xxx", "status": "DRAFT"}
    )

    assert 200 == response.status_code
    assert ServiceModificationHistoryItem.objects.exists()

    hitem = ServiceModificationHistoryItem.objects.first()

    assert hitem.user == user
    assert hitem.status == ""
