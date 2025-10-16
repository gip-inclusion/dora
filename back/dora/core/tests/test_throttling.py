import pytest
from django.core.cache import cache
from django.urls import path
from rest_framework.response import Response
from rest_framework.test import APITestCase
from rest_framework.throttling import AnonRateThrottle
from rest_framework.views import APIView

ANON_THROTTLE_RATE_PER_MINUTE = 24


class ThrottleTestView(APIView):
    permission_classes = []

    throttle_classes = [
        AnonRateThrottle,
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
                self.test_endpoint,
                HTTP_X_FORWARDED_FOR="192.168.1.100, 10.0.0.1, 10.0.0.2, 10.0.0.3",
            )
            self.assertEqual(response.status_code, 200)

        for i in range(int(ANON_THROTTLE_RATE_PER_MINUTE / 2)):
            response = self.client.get(
                self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100, 10.0.0.20"
            )
            self.assertEqual(response.status_code, 200)

        response_1 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100, 10.0.0.2, 10.0.0.3"
        )
        self.assertEqual(response_1.status_code, 429)
        response_2 = self.client.get(
            self.test_endpoint, HTTP_X_FORWARDED_FOR="192.168.1.100,10.0.0.20"
        )
        self.assertEqual(response_2.status_code, 429)
