import logging

import pytest
from django.conf import settings
from django.core.cache.backends.locmem import LocMemCache
from django.urls import reverse

import config.admin
from config.admin import AdminLoginAction
from dora.core.test_utils import make_user
from dora.logs.models import ActionLog

PASSWORD = "mot-de-passe-correct"


@pytest.fixture(autouse=True)
def isolated_cache(monkeypatch):
    # Le cache par défaut (Redis) est partagé entre les tests et entre les exécutions
    login_cache = LocMemCache("admin-login-tests", {})
    # Les instances de même nom partagent leur contenu
    login_cache.clear()
    monkeypatch.setattr(config.admin, "cache", login_cache)


@pytest.fixture
def staff_user():
    user = make_user(is_staff=True)
    user.set_password(PASSWORD)
    user.save()
    return user


def login(client, email, password, ip="127.0.0.1"):
    return client.post(
        reverse("admin:login"),
        {"username": email, "password": password},
        REMOTE_ADDR=ip,
    )


def test_successful_login_is_logged(client, staff_user):
    response = login(client, staff_user.email, PASSWORD)

    assert response.status_code == 302
    log = ActionLog.objects.get()
    assert log.payload["action"] == AdminLoginAction.SUCCEEDED
    assert log.payload["userId"] == staff_user.pk
    assert log.legal


def test_failed_login_is_logged(client, staff_user):
    response = login(client, staff_user.email, "mauvais")

    assert response.status_code == 200
    log = ActionLog.objects.get()
    assert log.payload["action"] == AdminLoginAction.FAILED
    assert log.payload["email"] == staff_user.email
    assert log.payload["ip"] == "127.0.0.1"
    assert "mauvais" not in str(log.payload)


def test_unknown_email_is_not_logged_in_clear(client, staff_user):
    # Mot de passe saisi par erreur dans le champ email
    login(client, PASSWORD, "mauvais")

    log = ActionLog.objects.get()
    assert "email" not in log.payload
    assert log.payload["emailDigest"]
    assert PASSWORD not in str(log.payload)


def last_log():
    return ActionLog.objects.order_by("created_at").last()


def test_login_blocked_after_max_failures_by_email(client, staff_user):
    for i in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_EMAIL):
        login(client, staff_user.email, "mauvais", ip=f"10.0.0.{i}")

    response = login(client, staff_user.email, PASSWORD, ip="10.0.1.1")

    assert response.status_code == 200
    assert "Trop de tentatives" in response.content.decode()
    assert last_log().payload["blocked"]


def test_login_blocked_after_max_failures_by_ip(client, staff_user):
    for i in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_IP):
        login(client, f"inconnu{i}@example.com", "mauvais")

    response = login(client, staff_user.email, PASSWORD)

    assert response.status_code == 200
    assert "Trop de tentatives" in response.content.decode()
    assert last_log().payload["blocked"]


def test_blocked_attempts_are_logged_outside_action_log(client, staff_user, caplog):
    for i in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_IP):
        login(client, f"inconnu{i}@example.com", "mauvais")

    with caplog.at_level(logging.WARNING, logger="dora.admin"):
        login(client, staff_user.email, PASSWORD)

    assert ActionLog.objects.count() == settings.ADMIN_LOGIN_MAX_FAILURES_PER_IP
    [record] = [r for r in caplog.records if r.name == "dora.admin"]
    assert "bloquée" in record.getMessage()
    assert staff_user.email not in record.getMessage()


def test_successful_login_resets_email_counter(client, staff_user):
    for i in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_EMAIL - 1):
        login(client, staff_user.email, "mauvais", ip=f"10.0.0.{i}")
    login(client, staff_user.email, PASSWORD, ip="10.0.1.1")
    client.logout()

    login(client, staff_user.email, "mauvais", ip="10.0.2.1")
    response = login(client, staff_user.email, PASSWORD, ip="10.0.3.1")

    assert response.status_code == 302


def test_empty_password_is_neither_counted_nor_resets_counter(client, staff_user):
    for i in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_EMAIL - 1):
        login(client, staff_user.email, "mauvais", ip=f"10.0.0.{i}")

    response = login(client, staff_user.email, "", ip="10.0.1.1")
    assert response.status_code == 200
    login(client, staff_user.email, "mauvais", ip="10.0.2.1")
    response = login(client, staff_user.email, PASSWORD, ip="10.0.3.1")

    assert "Trop de tentatives" in response.content.decode()


def test_successful_logins_are_not_counted_against_ip(client, staff_user):
    for _ in range(settings.ADMIN_LOGIN_MAX_FAILURES_PER_IP + 1):
        response = login(client, staff_user.email, PASSWORD)
        client.logout()

    assert response.status_code == 302
