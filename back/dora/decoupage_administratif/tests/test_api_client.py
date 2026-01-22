from unittest import mock

import pytest
import requests
from django.test import SimpleTestCase

from dora.decoupage_administratif.api_client import DecoupageAdministratifAPIClient


@pytest.mark.no_django_db
class DecoupageAdministratifAPIClientTests(SimpleTestCase):
    def setUp(self):
        self.session = mock.Mock()
        self.response = mock.Mock()
        self.response.json.return_value = [{"code": "dummy"}]
        self.response.raise_for_status.return_value = None
        self.session.get.return_value = self.response
        self.client = DecoupageAdministratifAPIClient(
            base_url="https://example.com",
            timeout_seconds=5,
            session=self.session,
        )

    def test_fetch_communes_calls_expected_endpoint(self):
        data = self.client.fetch_communes()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/communes",
            params={
                "fields": "code,nom,codeDepartement,codeRegion,codesPostaux,codeEpci,population,centre",
                "format": "json",
            },
            timeout=5,
        )

    def test_fetch_departements_calls_expected_endpoint(self):
        data = self.client.fetch_departements()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/departements",
            params={"fields": "code,nom,codeRegion", "format": "json"},
            timeout=5,
        )

    def test_fetch_epci_calls_expected_endpoint(self):
        data = self.client.fetch_epci()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/epcis",
            params={
                "fields": "code,nom,codesDepartements,codesRegions",
                "format": "json",
            },
            timeout=5,
        )

    def test_fetch_regions_calls_expected_endpoint(self):
        data = self.client.fetch_regions()

        self.assertEqual(data, self.response.json.return_value)
        self.session.get.assert_called_once_with(
            "https://example.com/regions",
            params={"fields": "code,nom", "format": "json"},
            timeout=5,
        )

    def test_fetch_communes_propagates_http_errors(self):
        http_error = requests.HTTPError("boom")
        self.response.raise_for_status.side_effect = http_error

        with self.assertRaises(requests.HTTPError):
            self.client.fetch_communes()
