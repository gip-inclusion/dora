from django.http import HttpResponseRedirect
from django.test import RequestFactory, TestCase, override_settings

from config.domain_redirect_middleware import DomainRedirectMiddleware


@override_settings(
    OLD_HOST="old-domain.com",
    NEW_HOST="new-domain.com",
    ALLOWED_HOSTS=["old-domain.com", "new-domain.com"],
)
class DomainRedirectMiddlewareTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.middleware = DomainRedirectMiddleware(get_response=lambda x: None)

    def test_redirects_old_host_to_new_host_when_http(self):
        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsInstance(response, HttpResponseRedirect)
        self.assertEqual(response.status_code, 307)
        self.assertEqual(response["Location"], "http://new-domain.com/api/test/")

    def test_https_redirect_preserved(self):
        request = self.factory.get(
            "/api/test/", HTTP_HOST="old-domain.com", secure=True
        )

        response = self.middleware.process_request(request)

        self.assertEqual(response.status_code, 307)
        self.assertEqual(response["Location"], "https://new-domain.com/api/test/")

    def test_preserves_query_parameters(self):
        request = self.factory.get(
            "/search/?q=test&page=2", HTTP_HOST="old-domain.com", secure=True
        )

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
    def test_no_redirect_when_both_env_vars_missing(self):
        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsNone(response)

    @override_settings(OLD_HOST=None)
    def test_no_redirect_when_one_env_var_missing(self):
        request = self.factory.get("/api/test/", HTTP_HOST="old-domain.com")

        response = self.middleware.process_request(request)

        self.assertIsNone(response)

    @override_settings(
        OLD_HOST="old-domain.com:8000",
        NEW_HOST="new-domain.com:8001",
    )
    def test_handles_different_ports(self):
        request = self.factory.get(
            "/api/test/", HTTP_HOST="old-domain.com:8000", secure=True
        )

        response = self.middleware.process_request(request)

        self.assertEqual(response["Location"], "https://new-domain.com:8001/api/test/")

    @override_settings(
        OLD_HOST="www.old-domain.com",
        NEW_HOST="www.new-domain.com",
        ALLOWED_HOSTS=["www.old-domain.com", "www.new-domain.com"],
    )
    def test_handles_www_subdomain(self):
        request = self.factory.get(
            "/api/test/", HTTP_HOST="www.old-domain.com", secure=True
        )

        response = self.middleware.process_request(request)

        self.assertEqual(response["Location"], "https://www.new-domain.com/api/test/")
