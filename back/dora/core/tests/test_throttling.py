from unittest.mock import Mock

from rest_framework.test import APITestCase

from dora.core.test_utils import make_structure
from dora.core.throttling import StructureUploadThrottle


class StructureUploadThrottleTestCase(APITestCase):
    def setUp(self):
        self.throttle = StructureUploadThrottle()
        self.structure = make_structure()

    def test_generates_correct_cache_key(self):
        """Le cache key généré contient le scope et le slug de la structure."""
        request = Mock()
        view = Mock()
        view.kwargs = {"structure_slug": self.structure.slug}

        cache_key = self.throttle.get_cache_key(request, view)

        self.assertIsNotNone(cache_key)
        self.assertIn("structure_upload", cache_key)
        self.assertIn(self.structure.slug, cache_key)

    def test_throttles_correctly_per_structure(self):
        structure2 = make_structure()

        self.throttle.rate = "3/min"
        self.throttle.num_requests, self.throttle.duration = self.throttle.parse_rate(
            self.throttle.rate
        )

        request = Mock()
        view = Mock()
        view.kwargs = {"structure_slug": self.structure.slug}

        for i in range(3):
            allowed = self.throttle.allow_request(request, view)
            self.assertTrue(allowed, f"La requête {i + 1}/3 devrait être autorisée")

        allowed = self.throttle.allow_request(request, view)
        self.assertFalse(allowed, "La 4ème requête devrait être bloquée")

        view.kwargs = {"structure_slug": structure2.slug}
        for i in range(3):
            allowed = self.throttle.allow_request(request, view)
            self.assertTrue(
                allowed,
                f"Structure2 devrait avoir ses propres limites (requête {i + 1}/3)",
            )

        allowed = self.throttle.allow_request(request, view)
        self.assertFalse(allowed)
