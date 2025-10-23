from rest_framework.test import APITestCase

from dora.core.test_utils import make_user
from dora.users.models import ConsentRecord


class ConsentRecordTestCase(APITestCase):
    def test_create_consent_record_for_anonymous_user(self):
        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_user_hash": "12345abcdef",
                "consent_version": "1.1",
                "consent_choices": {
                    "google_cse": True,
                    "matomo": True,
                },
            },
        )

        self.assertEqual(response.status_code, 201)

        consent_record = ConsentRecord.objects.last()

        self.assertEqual(consent_record.anonymous_user_hash, "12345abcdef")
        self.assertEqual(consent_record.user, None)
        self.assertEqual(
            consent_record.consent_version,
            "1.1",
        )
        self.assertEqual(
            consent_record.consent_choices,
            {
                "google_cse": True,
                "matomo": True,
            },
        )

    def test_create_consent_record_for_authenticated_user(self):
        user = make_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_user_hash": "12345abcdef",
                "consent_version": "1.2",
                "consent_choices": {
                    "google_cse": False,
                    "matomo": False,
                },
            },
        )

        self.assertEqual(response.status_code, 201)

        consent_record = ConsentRecord.objects.last()

        self.assertEqual(consent_record.user, user)
        self.assertEqual(consent_record.anonymous_user_hash, None)
        self.assertEqual(
            consent_record.consent_version,
            "1.2",
        )
        self.assertEqual(
            consent_record.consent_choices,
            {
                "google_cse": False,
                "matomo": False,
            },
        )

    def test_raise_validation_error_when_neither_user_nor_anonymous_user_hash(self):
        response = self.client.post(
            "/consent-record/",
            {"consent_version": "1.1", "consent_choices": {}},
        )

        self.assertEqual(response.status_code, 400)
        self.assertEqual(
            str(response.data["non_field_errors"][0]["message"]),
            "Doit fournir anonymous_user_hash ou être connecté",
        )

    def test_raise_validation_error_when_consent_choices_not_a_dict(self):
        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_user_hash": "12345abcdef",
                "consent_version": "1.2",
                "consent_choices": "abc",
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_raise_validation_error_when_consent_choices_invalid(self):
        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_user_hash": "12345abcdef",
                "consent_version": "1.2",
                "consent_choices": {
                    "google_cse": "abc",
                    "matomo": False,
                },
            },
        )

        self.assertEqual(response.status_code, 400)

    def test_anonymous_user_id_as_empty_string_raises_400_when_anonymous_user(self):
        """
        Si l'utilisateur est connecté, on sauvegarde son id dans la colonne `user`
        et anonymous_user_hash est None
        """
        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_user_hash": "",
                "consent_version": "1.2",
                "consent_choices": {
                    "google_cse": False,
                    "matomo": False,
                },
            },
        )

        self.assertEqual(response.status_code, 400)
