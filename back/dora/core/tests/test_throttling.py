from unittest.mock import Mock

import pytest
from django.contrib.auth.models import AnonymousUser
from django.core.cache.backends.locmem import LocMemCache
from django.test import RequestFactory
from rest_framework.request import Request
from rest_framework.test import APITestCase
from rest_framework.throttling import AnonRateThrottle

from dora.core.test_utils import make_structure
from dora.core.throttling import StructureUploadThrottle


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
