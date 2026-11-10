import json
import logging

import pytest
from django.test import RequestFactory

from dora.core.log_formatters import DataDogJSONFormatter


@pytest.mark.no_django_db
def test_log_client_ip_ignores_spoofed_forwarded_for(monkeypatch):
    request = RequestFactory().get(
        "/", HTTP_X_FORWARDED_FOR="198.51.100.1, 203.0.113.7"
    )
    monkeypatch.setattr("django_datadog_logger.wsgi.get_wsgi_request", lambda: request)
    record = logging.makeLogRecord({"msg": "message", "levelname": "INFO"})

    log_entry = json.loads(DataDogJSONFormatter().format(record))

    assert log_entry["network.client.ip"] == "203.0.113.7"


@pytest.mark.no_django_db
def test_log_without_request_has_no_client_ip(monkeypatch):
    monkeypatch.setattr("django_datadog_logger.wsgi.get_wsgi_request", lambda: None)
    record = logging.makeLogRecord({"msg": "message", "levelname": "INFO"})

    log_entry = json.loads(DataDogJSONFormatter().format(record))

    assert "network.client.ip" not in log_entry
