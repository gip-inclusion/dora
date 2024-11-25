import json
from unittest.mock import Mock, patch

from django.contrib.gis.geos import Point

from dora.core.constants import WGS84
from dora.core.test_utils import make_service
from dora.services.utils import update_geom


class TestUpdateServiceGeom:
    @patch("dora.services.utils.requests.get")
    def test_update_geom_should_add_service_geom_when_location_found(self, mock_get):
        # Given
        service = make_service()
        service.geom = None
        service.address1 = "24 Rue du Commandant Guilbaud"
        service.address2 = ""
        service.postal_code = "75016"
        service.city = "Paris"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [
                    {
                        "geometry": {
                            "type": "Point",
                            "coordinates": [2.251558, 48.84186],
                        },
                        "properties": {
                            "score": 0.9706190909090909,
                            "postcode": "75016",
                            "citycode": "75116",
                            "city": "Paris",
                        },
                    }
                ],
            }
        ).encode("utf-8")
        mock_get.return_value = mock_response

        # When
        update_geom(service)

        # Then
        assert service.geom is not None
        assert service.geom.x == 2.251558
        assert service.geom.y == 48.84186
        assert service.geom.srid == WGS84

    @patch("dora.services.utils.requests.get")
    def test_update_geom_should_change_service_geom_even_when_it_is_already_defined(
        self, mock_get
    ):
        # Given
        initial_geom = Point(2.251558, 48.84186, srid=WGS84)
        service = make_service()
        service.geom = initial_geom
        service.address1 = "24 Rue du Commandant Guilbaud"
        service.address2 = ""
        service.postal_code = "75016"
        service.city = "Paris"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [
                    {
                        "geometry": {
                            "type": "Point",
                            "coordinates": [1.434047, 43.583313],
                        },
                        "properties": {
                            "score": 0.9706190909090909,
                            "postcode": "31000",
                            "citycode": "31300",
                            "city": "Toulouse",
                        },
                    }
                ],
            }
        ).encode("utf-8")
        mock_get.return_value = mock_response

        # When
        update_geom(service)

        # Then
        assert service.geom.x == 1.434047
        assert service.geom.y == 43.583313
        assert service.geom.srid == WGS84
        # warning: other location data does not change
        service.city == "Paris"
        service.postal_code = "75016"

    @patch("dora.services.utils.requests.get")
    def test_update_geom_should_keep_service_geom_to_None_when_location_not_found(
        self, mock_get
    ):
        # Given
        service = make_service()
        service.geom = None
        service.address1 = "Lieu improbable"
        service.address2 = ""
        service.postal_code = "98000"
        service.city = "Anywhereland"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [],
            }
        ).encode("utf-8")
        mock_get.return_value = mock_response

        # When
        update_geom(service)

        # Then
        assert service.geom is None

    @patch("dora.services.utils.requests.get")
    def test_update_geom_should_keep_service_geom_to_None_when_score_is_low(
        self, mock_get
    ):
        # Given
        service = make_service()
        service.geom = None
        service.address1 = "Lieu improbable"
        service.address2 = ""
        service.postal_code = "98000"
        service.city = "Anywhereland"

        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.content = json.dumps(
            {
                "features": [
                    {"properties": {"score": 0.20}},
                ],
            }
        ).encode("utf-8")
        mock_get.return_value = mock_response

        # When
        update_geom(service)

        # Then
        assert service.geom is None

    @patch("dora.services.utils.requests.get")
    def test_update_geom_should_keep_service_geom_to_None_when_api_error(
        self, mock_get
    ):
        # Given
        service = make_service()
        service.geom = None
        service.address1 = "Lieu improbable"
        service.address2 = ""
        service.postal_code = "98000"
        service.city = "Anywhereland"

        mock_response = Mock()
        mock_response.status_code = 500
        mock_get.return_value = mock_response

        # When
        update_geom(service)

        # Then
        assert service.geom is None
