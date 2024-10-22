from io import StringIO

import pytest
from django.conf import settings


@pytest.fixture
def notifications_disabled():
    old_value, settings.NOTIFICATIONS_ENABLED = settings.NOTIFICATIONS_ENABLED, None
    yield
    settings.NOTIFICATIONS_ENABLED = old_value


@pytest.fixture
def notifications_enabled():
    old_value, settings.NOTIFICATIONS_ENABLED = settings.NOTIFICATIONS_ENABLED, "True"
    yield
    settings.NOTIFICATIONS_ENABLED = old_value


@pytest.fixture
def with_limit(notifications_enabled):
    old_value, settings.NOTIFICATIONS_LIMIT = settings.NOTIFICATIONS_LIMIT, 10
    yield
    settings.NOTIFICATIONS_LIMIT = old_value


@pytest.fixture
def with_types(notifications_enabled):
    old_value, settings.NOTIFICATIONS_TASK_TYPES = (
        settings.NOTIFICATIONS_TASK_TYPES,
        "orphan_structures",
    )
    yield
    settings.NOTIFICATIONS_TASK_TYPES = old_value


@pytest.fixture
def stdout():
    return StringIO()
