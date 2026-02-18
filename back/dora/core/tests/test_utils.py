import json
from unittest import TestCase
from unittest.mock import Mock, patch

import pytest
from django.contrib.gis.geos import Point
from django.http import HttpResponse
from django.test import override_settings

from dora.core import utils
from dora.core.constants import WGS84
from dora.core.utils import address_to_one_line, set_auth_token_cookie


class UtilsTestCase(TestCase):
    def test_normalize_description(self):
        cases = [
            (
                "Lorem ipsum dolor sit amet",
                10,
                ("Lorem ips…", "Lorem ipsum dolor sit amet"),
            ),
            (
                "Lorem ipsum dolor sit amet",
                100,
                ("Lorem ipsum dolor sit amet", ""),
            ),
        ]

        for input, limit, expected in cases:
            self.assertEqual(utils.normalize_description(input, limit), expected)

    def test_normalize_phone_number(self):
        cases = [
            ("01-02-03 04.05", "0102030405"),
            ("0102030405 - 0203040506", "0102030405"),
            ("3509", "3509"),
            ("01 02 03 04 05", "0102030405"),
            ("a01c02-03 04 05", "0102030405"),
            ("+33 01 02 03 04 05", "0102030405"),
            ("+33 (0)1 02 03 04 05", "0102030405"),
            ("+33 1 02 03 04 05", "0102030405"),
            ("+33 1 +33 03 33 05", "0133033305"),
        ]

        for input_number, expected_number in cases:
            self.assertEqual(
                expected_number,
                utils.normalize_phone_number(input_number),
            )

    @patch("dora.core.utils.requests.get")
    def test_get_geo_data_successful(self, mock_requests_get):
        # Given
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [
                    {
                        "geometry": {"coordinates": [2.351499, 48.856696]},
                        "properties": {
                            "score": 0.9,
                            "name": "24 Rue du Commandant Guilbaud",
                            "city": "Paris",
                            "postcode": "75016",
                            "citycode": "75116",
                        },
                    }
                ]
            }
        ).encode("utf-8")
        mock_requests_get.return_value = mock_response

        # When
        result = utils.get_geo_data(
            address="24 Rue du Commandant Guilbaud",
            city="Paris",
            postal_code="75016",
            city_code="75116",
        )

        # Then
        assert isinstance(result, utils.GeoData)
        assert result.address == "24 Rue du Commandant Guilbaud"
        assert result.city == "Paris"
        assert result.postal_code == "75016"
        assert result.city_code == "75116"
        assert isinstance(result.geom, Point)
        assert result.geom.x == 2.351499
        assert result.geom.y == 48.856696
        assert result.geom.srid == WGS84

    @patch("dora.core.utils.requests.get")
    def test_get_geo_data_no_features(self, mock_requests_get):
        # Given
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps({"features": []}).encode("utf-8")
        mock_requests_get.return_value = mock_response

        # When
        result = utils.get_geo_data(address="Nonexistent Place")

        # Then
        assert result is None

    @patch("dora.core.utils.requests.get")
    def test_get_geo_data_low_score(self, mock_requests_get):
        # Given
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [
                    {
                        "geometry": {"coordinates": [2.351499, 48.856696]},
                        "properties": {
                            "score": 0.4,  # Below threshold
                            "name": "24 Rue du Commandant Guilbaud",
                            "city": "Paris",
                            "postcode": "75016",
                            "citycode": "75116",
                        },
                    }
                ]
            }
        ).encode("utf-8")
        mock_requests_get.return_value = mock_response

        # When
        result = utils.get_geo_data(address="24 Rue du Commandant Guilbaud")

        # Then
        assert result is None

    @patch("dora.core.utils.requests.get")
    def test_get_geo_data_api_error(self, mock_requests_get):
        # Given
        mock_response = Mock()
        mock_response.status_code = 500
        mock_response.content = "Internal Server Error".encode("utf-8")
        mock_requests_get.return_value = mock_response

        # When
        result = utils.get_geo_data(address="24 Rue du Commandant Guilbaud")

        # Then
        assert result is None

    @patch("dora.core.utils.requests.get")
    def test_get_geo_data_invalid_json(self, mock_requests_get):
        # Given
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = "Invalid JSON".encode("utf-8")  # Not valid JSON
        mock_requests_get.return_value = mock_response

        # When / Then
        with self.assertRaises(json.JSONDecodeError):
            utils.get_geo_data(address="24 Rue du Commandant Guilbaud")


@pytest.mark.parametrize(
    "address1,address2,postal_code,city,expected",
    [
        (
            "6 Boulevard St Denis",
            "Plateforme de l'inclusion",
            "75010",
            "Paris",
            "6 Boulevard St Denis Plateforme de l'inclusion - 75010 Paris",
        ),
        (
            "6 Boulevard St Denis",
            None,
            "75010",
            "Paris",
            "6 Boulevard St Denis - 75010 Paris",
        ),
        (
            "6 Boulevard St Denis",
            "",
            "75010",
            "Paris",
            "6 Boulevard St Denis - 75010 Paris",
        ),
        (
            None,
            "Plateforme de l'inclusion",
            "75010",
            "",
            "Plateforme de l'inclusion - 75010",
        ),
        (
            "",
            "Plateforme de l'inclusion",
            "75010",
            None,
            "Plateforme de l'inclusion - 75010",
        ),
        (
            "6 Boulevard St Denis",
            "Plateforme de l'inclusion",
            None,
            "",
            "6 Boulevard St Denis Plateforme de l'inclusion",
        ),
        (
            "",
            "",
            "75010",
            "Paris",
            "75010 Paris",
        ),
        (
            "",
            "",
            "",
            "",
            "",
        ),
    ],
)
def test_address_to_one_line(address1, address2, postal_code, city, expected):
    assert address_to_one_line(address1, address2, postal_code, city) == expected


@override_settings(FRONTEND_URL="https://subdomain.example.com")
def test_set_auth_token_cookie():
    """set_auth_token_cookie définit le cookie avec les bons attributs."""
    response = HttpResponse()
    token_key = "test-token-key-12345"

    set_auth_token_cookie(response, token_key)

    assert "token" in response.cookies

    cookie = response.cookies["token"]
    assert cookie.value == token_key
    assert cookie["path"] == "/"
    assert cookie["samesite"] == "Lax"
    assert cookie["secure"] is True
    assert cookie.get("httponly", "") != "HttpOnly"
    assert cookie["domain"] == "subdomain.example.com"
