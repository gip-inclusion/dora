import pytest
from django.core.cache import cache
from django.urls import path
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.views import APIView

from dora.core.test_utils import make_user
from dora.core.throttling import ClientIPAnonRateThrottle

ANON_THROTTLE_RATE_PER_MINUTE = 24


class ThrottleTestView(APIView):
    permission_classes = []

    throttle_classes = [
        ClientIPAnonRateThrottle,
    ]

    def get(self, request):
        return Response({"message": "success"})


urlpatterns = [
    path("test-throttle/", ThrottleTestView.as_view()),
]


@pytest.mark.urls("dora.core.tests.test_throttling")
class ThrottlingTestCase(APITestCase):
    def setUp(self):
        cache.clear()

        self.test_endpoint = "/test-throttle/"
        self.client.force_authenticate(user=None)

    def test_anonymous_throttle_by_ip(self):
        for i in range(ANON_THROTTLE_RATE_PER_MINUTE):
            response = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100"
            )
            self.assertEqual(response.status_code, 200)

        response = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100"
        )
        self.assertEqual(response.status_code, 429)

    def test_different_ips_throttled_separately(self):
        for i in range(ANON_THROTTLE_RATE_PER_MINUTE):
            self.client.get(self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100")

        response = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.101"
        )
        self.assertEqual(response.status_code, 200)

    def test_authenticated_not_affected_by_anon_throttle(self):
        for i in range(ANON_THROTTLE_RATE_PER_MINUTE):
            self.client.get(self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100")

        user = make_user()
        self.client.force_authenticate(user=user)
        response = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100"
        )
        self.assertEqual(response.status_code, 200)

    def test_missing_x_forwarded_for_fallback(self):
        for i in range(ANON_THROTTLE_RATE_PER_MINUTE):
            response = self.client.get(self.test_endpoint)
            if i < ANON_THROTTLE_RATE_PER_MINUTE:
                self.assertEqual(response.status_code, 200)

        response = self.client.get(self.test_endpoint)
        self.assertEqual(response.status_code, 429)

    def test_should_throttle_different_ips_with_same_proxy(self):
        for i in range(ANON_THROTTLE_RATE_PER_MINUTE):
            response_1 = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.1"
            )
            self.assertEqual(response_1.status_code, 200)
            response_2 = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.101,10.0.0.1"
            )
            self.assertEqual(response_2.status_code, 200)

        response_1 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.1"
        )
        self.assertEqual(response_1.status_code, 429)
        response_2 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.101,10.0.0.1"
        )
        self.assertEqual(response_2.status_code, 429)

    def test_should_throttle_same_ip_with_different_proxies(self):
        for i in range(int(ANON_THROTTLE_RATE_PER_MINUTE / 2)):
            response = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.1"
            )
            self.assertEqual(response.status_code, 200)

        for i in range(int(ANON_THROTTLE_RATE_PER_MINUTE / 2)):
            response = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.2"
            )
            self.assertEqual(response.status_code, 200)

        response_1 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.1"
        )
        self.assertEqual(response_1.status_code, 429)
        response_2 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.2"
        )
        self.assertEqual(response_2.status_code, 429)
