import logging

import pytest
from django.core.exceptions import ValidationError

from .core import ActionLogHandler
from .models import ActionLog

# inutile de tester les fonctions héritées de logging.Logger et logging.Handler (filtre, niveau ...)


@pytest.fixture
def logger():
    return logging.getLogger("dora.logs.core")


def test_logger_created(logger):
    # le logger 'dora.logs.core' doit exister et avoir le bon handler
    [handler] = logger.handlers

    assert isinstance(handler, ActionLogHandler)


def test_store_log(logger):
    ActionLog(
        msg="ok", level=logging.DEBUG, legal=True, payload={"myInt": 42, "myBool": True}
    ).save()

    result = ActionLog.objects.first()

    assert result
    assert result.msg == "ok"
    assert result.level == logging.DEBUG
    assert result.legal
    assert result.payload.get("myInt") == 42
    assert result.payload.get("myBool")


def test_log_me(logger):
    logger.critical("Message important", {"unParam": "au hasard", "legal": True})

    result = ActionLog.objects.first()

    assert result
    assert result.msg == "Message important"
    assert result.level == logging.CRITICAL
    assert result.payload.get("unParam") == "au hasard"

    # le champ "legal" peut être modifié une fois l'objet créé,
    # mais si il est inclus dans le payload, le champ du modèle est initialisé
    # (et retiré du payload)
    assert result.legal
    assert "legal" not in result.payload.keys()


def test_str(logger):
    logger.error("Message texte", {"unParam": "au hasard", "legal": True})
    result = ActionLog.objects.first()

    assert str(result.pk) in str(result)

    assert "_legal" in result.__repr__()
    assert "_id" in result.__repr__()
    assert "_createdAt" in result.__repr__()
    assert "_level" in result.__repr__()


def test_bad_legal_in_json(logger):
    with pytest.raises(ValidationError):
        logger.critical("Message important", {"unParam": "au hasard", "legal": "no"})
