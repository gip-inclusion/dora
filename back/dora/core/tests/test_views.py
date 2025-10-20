from rest_framework.test import APITestCase

from dora.core.models import ConsentRecord
from dora.core.test_utils import make_user


class ConsentRecordTestCase(APITestCase):
    def test_create_consent_record_for_anonymous_user(self):
        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_id": "12345abcdef",
                "consent_version": "1.1",
                "consented_to_google": True,
                "consented_to_matomo": True,
            },
        )

        self.assertEqual(response.status_code, 201)

        consent_record = ConsentRecord.objects.last()

        self.assertEqual(consent_record.anonymous_id, "12345abcdef")
        self.assertEqual(consent_record.user, None)
        self.assertEqual(
            consent_record.consent_version,
            "1.1",
        )
        self.assertEqual(
            consent_record.consented_to_google,
            True,
        )
        self.assertEqual(
            consent_record.consented_to_matomo,
            True,
        )

    def test_create_consent_record_for_authenticated_user(self):
        user = make_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/consent-record/",
            {
                "anonymous_id": "12345abcdef",
                "consent_version": "1.2",
                "consented_to_google": False,
                "consented_to_matomo": True,
            },
        )

        self.assertEqual(response.status_code, 201)

        consent_record = ConsentRecord.objects.last()

        self.assertEqual(consent_record.user, user)
        self.assertEqual(consent_record.anonymous_id, None)
        self.assertEqual(
            consent_record.consent_version,
            "1.2",
        )
        self.assertEqual(
            consent_record.consented_to_google,
            False,
        )
        self.assertEqual(
            consent_record.consented_to_matomo,
            True,
        )

    def test_raise_validation_error_when_neither_user_nor_anonymous_id(self):
        response = self.client.post(
            "/consent-record/",
            {
                "consent_version": "1.1",
                "consented_to_google": True,
                "consented_to_matomo": True,
            },
        )

        self.assertEqual(response.status_code, 400)
