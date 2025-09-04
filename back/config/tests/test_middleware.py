import os

from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase, override_settings

from config.domain_redirect_middleware import DomainRedirectMiddleware


@override_settings(
    OLD_HOST="old-domain.com", NEW_HOST="new-domain.com", ALLOWED_HOSTS=["*"]
)
class DomainRedirectMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DomainRedirectMiddleware(get_response=lambda x: None)

    def test_redirects_old_host_to_new_host(self):
        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response["Location"], "https://new-domain.com/api/test/")

    def test_preserves_query_parameters(self):
        request = self.factory.get("/search/?q=test&page=2", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertEqual(
            response["Location"], "https://new-domain.com/search/?q=test&page=2"
        )

    def test_preserves_post_data_with_307(self):
        request = self.factory.post(
            "/api/create/", {"name": "test"}, HTTP_HOST="old-domain.com"
        )

        response = self.middleware.process_request(request)

        self.assertEqual(response.status_code, 307)

    def test_no_redirect_for_new_host(self):
        request = self.factory.get("/api/test/", HTTP_HOST="new-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsNone(response)

    @override_settings(OLD_HOST=None, NEW_HOST=None)
    def test_no_redirect_when_env_vars_missing(self):
        os.environ.pop("OLD_HOST", None)
        os.environ.pop("NEW_HOST", None)

        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsNone(response)

    @override_settings(
        OLD_HOST="old-domain.com:8000",
        NEW_HOST="new-domain.com:8000",
    )
    def test_handles_different_ports(self):
        os.environ["OLD_HOST"] = "old-domain.com:8000"
        os.environ["NEW_HOST"] = "new-domain.com:8000"

        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com:8000")

        response = self.middleware.process_request(request)

        self.assertEqual(response["Location"], "https://new-domain.com:8000/api/test/")

    def test_handles_www_subdomain(self):
        request = self.factory.get("/api/test/", HTTP_HOST="www.old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsNone(response)
