from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.cache.backends.locmem import LocMemCache
from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.test import APITestCase
from rest_framework.throttling import AnonRateThrottle

from dora.core.test_utils import make_structure
from dora.core.throttling import (
    ClientIpAnonRateThrottle,
    StructureUploadThrottle,
    get_front_client_ip,
)


class StructureUploadThrottleTestCase(APITestCase):
    def setUp(self):
        self.throttle = StructureUploadThrottle()
        self.structure = make_structure()

    def test_throttles_correctly_per_structure(self):
        structure2 = make_structure()

        self.throttle.rate = "3/min"
        self.throttle.num_requests, self.throttle.duration = self.throttle.parse_rate(
            self.throttle.rate
        )

        request = Mock()
        view = Mock()
        request.resolver_match.kwargs = {"structure_slug": self.structure.slug}

        for i in range(3):
            allowed = self.throttle.allow_request(request, view)
            self.assertTrue(allowed, f"La requête {i + 1}/3 devrait être autorisée")

        allowed = self.throttle.allow_request(request, view)
        self.assertFalse(allowed, "La 4ème requête devrait être bloquée")

        request.resolver_match.kwargs = {"structure_slug": structure2.slug}
        for i in range(3):
            allowed = self.throttle.allow_request(request, view)
            self.assertTrue(
                allowed,
                f"Structure2 devrait avoir ses propres limites (requête {i + 1}/3)",
            )

        allowed = self.throttle.allow_request(request, view)
        self.assertFalse(allowed)


def make_throttle(throttle_class, rate="2/min"):
    throttle = throttle_class()
    throttle.rate = rate
    throttle.num_requests, throttle.duration = throttle.parse_rate(rate)
    throttle.cache = LocMemCache("throttling-tests", {})
    return throttle


def anonymous_request(**meta):
    request = Request(RequestFactory().get("/", **meta))
    request.user = AnonymousUser()
    return request


@pytest.mark.no_django_db
def test_anon_throttle_cannot_be_bypassed_by_spoofing_x_forwarded_for():
    throttle = make_throttle(AnonRateThrottle)

    def allow(spoofed_ip):
        request = anonymous_request(HTTP_X_FORWARDED_FOR=f"{spoofed_ip}, 203.0.113.7")
        return throttle.allow_request(request, view=None)

    assert allow("192.0.2.1")
    assert allow("192.0.2.2")
    assert not allow("192.0.2.3")


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "configured_secret,meta,expected",
    [
        ("s3cret", {"HTTP_X_DORA_PROXY_SECRET": "s3cret"}, "192.0.2.1"),
        ("s3cret", {"HTTP_X_DORA_PROXY_SECRET": "faux"}, None),
        ("s3cret", {}, None),
        # Sans secret configuré, l'en-tête n'est jamais accepté
        ("", {"HTTP_X_DORA_PROXY_SECRET": ""}, None),
    ],
)
def test_get_front_client_ip(settings, configured_secret, meta, expected):
    settings.FRONT_PROXY_SECRET = configured_secret
    request = RequestFactory().get("/", HTTP_X_DORA_CLIENT_IP="192.0.2.1", **meta)
    assert get_front_client_ip(request) == expected


@pytest.mark.no_django_db
@pytest.mark.parametrize(
    "meta,expected",
    [
        (
            {
                "HTTP_X_DORA_PROXY_SECRET": "s3cret",
                "HTTP_X_DORA_CLIENT_IP": "192.0.2.1",
            },
            "192.0.2.1",
        ),
        # IP du front non authentifiée : dernière adresse de X-Forwarded-For
        ({"HTTP_X_DORA_CLIENT_IP": "192.0.2.1"}, "203.0.113.7"),
    ],
)
def test_client_ip_throttle_ident(settings, meta, expected):
    settings.FRONT_PROXY_SECRET = "s3cret"
    request = anonymous_request(
        HTTP_X_FORWARDED_FOR="198.51.100.1, 203.0.113.7", **meta
    )
    assert ClientIpAnonRateThrottle().get_ident(request) == expected
