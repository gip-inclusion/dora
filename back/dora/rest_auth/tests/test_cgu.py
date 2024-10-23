from datetime import timedelta

from django.utils import timezone
from freezegun import freeze_time
from model_bakery import baker
from rest_framework.test import APITestCase

DUMMY_SIRET = "12345678901234"


class CguTestCase(APITestCase):
    def test_no_cgu(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/")
        self.assertEqual(response.status_code, 400)

    def test_user_accepts_cgu(self):
        cgu_version = "20230714"
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(cgu_version, user.cgu_versions_accepted)

    def test_user_accepts_new_cgu_version(self):
        old_cgu_version = "20230715"
        cgu_version = "20230722"
        user = baker.make(
            "users.User",
            is_valid=True,
            cgu_versions_accepted={old_cgu_version: "2021-07-22T00:00:00+00:00"},
        )
        self.client.force_authenticate(user=user)
        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(old_cgu_version, user.cgu_versions_accepted)
        self.assertIn(cgu_version, user.cgu_versions_accepted)

    def test_no_overwrite_already_valided_cgu(self):
        cgu_version = "20230714"
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)

        response = self.client.post("/auth/accept-cgu/", {"cgu_version": cgu_version})
        user.refresh_from_db()
        self.assertEqual(response.status_code, 204)
        self.assertIn(cgu_version, user.cgu_versions_accepted)
        cgu_validation_datetime = user.cgu_versions_accepted[cgu_version]

        with freeze_time(timezone.now() + timedelta(days=2)):
            response = self.client.post(
                "/auth/accept-cgu/", {"cgu_version": cgu_version}
            )
            user.refresh_from_db()
            self.assertEqual(response.status_code, 204)
            self.assertIn(cgu_version, user.cgu_versions_accepted)
            self.assertEqual(
                cgu_validation_datetime, user.cgu_versions_accepted[cgu_version]
            )
