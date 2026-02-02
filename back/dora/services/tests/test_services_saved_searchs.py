from datetime import timedelta
from io import StringIO
from unittest import mock

from django.contrib.gis.geos import Point
from django.core import mail
from django.core.management import call_command
from django.utils import timezone
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.constants import WGS84
from dora.core.test_utils import make_service
from dora.data_inclusion.test_utils import FakeDataInclusionClient
from dora.decoupage_administratif.models import (
    AdminDivisionType,
    City,
    Department,
    Region,
)
from dora.services.enums import ServiceStatus
from dora.services.management.commands.send_saved_searches_notifications import (
    get_saved_search_notifications_to_send,
)

from ..models import SavedSearch, SavedSearchFrequency

SAVE_SEARCH_ARGS = {
    "category": "choisir-un-metier",
    "subcategories": [
        "choisir-un-metier--confirmer-son-choix-de-metier",
        "choisir-un-metier--connaitre-les-opportunites-demploi",
    ],
    "city_code": "58211",
    "city_label": "Poil (58)",
    "kinds": ["aide-financiere", "aide-materielle"],
    "fees": ["gratuit", "payant"],
    "funding_labels": ["funding-label-1", "funding-label-2"],
}


class ServiceSavedSearchTestCase(APITestCase):
    def setUp(self):
        self.di_client = FakeDataInclusionClient()
        self.patcher = mock.patch("dora.data_inclusion.di_client_factory")
        self.mock_di_client_factory = self.patcher.start()
        self.mock_di_client_factory.return_value = self.di_client

    def tearDown(self):
        self.patcher.stop()

    def test_cant_create_search_if_no_logged_user(self):
        response = self.client.post("/saved-searches/", SAVE_SEARCH_ARGS)
        self.assertEqual(response.status_code, 401)

    def test_missing_required_fields(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)

        for property in ["city_code", "city_label"]:
            args = SAVE_SEARCH_ARGS.copy()
            del args[property]
            response = self.client.post("/saved-searches/", args)
            self.assertEqual(response.status_code, 400)

    def test_create_search(self):
        baker.make(
            "FundingLabel",
            value=SAVE_SEARCH_ARGS.get("funding_labels")[0],
            label=SAVE_SEARCH_ARGS.get("funding_labels")[0],
        )
        baker.make(
            "FundingLabel",
            value=SAVE_SEARCH_ARGS.get("funding_labels")[1],
            label=SAVE_SEARCH_ARGS.get("funding_labels")[1],
        )

        self.assertEqual(SavedSearch.objects.all().count(), 0)

        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.post("/saved-searches/", SAVE_SEARCH_ARGS)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(SavedSearch.objects.all().count(), 1)

        saved_search = SavedSearch.objects.first()
        self.assertEqual(
            sorted(list(saved_search.subcategories.values_list("value", flat=True))),
            sorted(SAVE_SEARCH_ARGS.get("subcategories")),
        )
        self.assertEqual(
            sorted(list(saved_search.funding_labels.values_list("value", flat=True))),
            sorted(SAVE_SEARCH_ARGS.get("funding_labels")),
        )

    def test_delete_search(self):
        user = baker.make("users.User", is_valid=True)
        saved_search = baker.make(
            "SavedSearch",
            user=user,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
        )
        self.assertEqual(SavedSearch.objects.all().count(), 1)

        self.client.force_authenticate(user=user)
        response = self.client.delete(f"/saved-searches/{saved_search.id}/")
        self.assertEqual(SavedSearch.objects.all().count(), 0)
        self.assertEqual(response.status_code, 204)

    def test_delete_search_wrong_user(self):
        user = baker.make("users.User", is_valid=True)
        user2 = baker.make("users.User", is_valid=True)
        saved_search = baker.make(
            "SavedSearch",
            user=user,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
        )
        self.assertEqual(SavedSearch.objects.all().count(), 1)

        self.client.force_authenticate(user=user2)
        response = self.client.delete(f"/saved-searches/{saved_search.id}/")

        self.assertEqual(response.status_code, 404)
        self.assertEqual(SavedSearch.objects.all().count(), 1)

    def test_delete_search_not_existing(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.delete("/saved-searches/123/")
        self.assertEqual(SavedSearch.objects.all().count(), 0)
        self.assertEqual(response.status_code, 404)

    def test_update_search_not_existing(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)
        response = self.client.patch("/saved-searches/xxx/", {"frequency": "NEVER"})
        self.assertEqual(response.status_code, 404)

    def test_update_frequency_not_existing(self):
        user = baker.make("users.User", is_valid=True)
        saved_search = baker.make(
            "SavedSearch",
            user=user,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
        )
        self.client.force_authenticate(user=user)
        response = self.client.patch(
            f"/saved-searches/{saved_search.id}/",
            {"frequency": "xxx"},
        )
        self.assertEqual(response.status_code, 400)

    def test_update_frequency_ok(self):
        user = baker.make("users.User", is_valid=True)
        self.client.force_authenticate(user=user)

        saved_search = baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.TWO_WEEKS,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
        )
        self.assertEqual(
            saved_search.frequency,
            SavedSearchFrequency.TWO_WEEKS,
        )

        response = self.client.patch(
            f"/saved-searches/{saved_search.id}/",
            {"frequency": "NEVER"},
        )
        self.assertEqual(response.status_code, 200)

        saved_search.refresh_from_db()
        self.assertEqual(
            saved_search.frequency,
            SavedSearchFrequency.NEVER,
        )


class ServiceSavedSearchNotificationTestCase(APITestCase):
    def setUp(self):
        region = baker.make(Region, code="027", name="Bourgogne-Franche-Comté")
        baker.make(
            Department,
            code="58",
            name="Nièvre",
            region=region.code,
        )
        baker.make(
            City,
            code="58211",
            name="Poil",
            department="58",
            region=region.code,
            epci="200000000",
            center=Point(3.0, 47.0, srid=WGS84),
        )
        self.service_name = "serviceName"

        self.di_client = FakeDataInclusionClient()
        self.patcher = mock.patch("dora.data_inclusion.di_client_factory")
        self.mock_di_client_factory = self.patcher.start()
        self.mock_di_client_factory.return_value = self.di_client

    def tearDown(self):
        self.patcher.stop()

    def call_command(self):
        call_command("send_saved_searches_notifications", stdout=StringIO())

    def test_get_monthly_saved_searches(self):
        # ÉTANT DONNÉ un utilisateur avec deux notifications mensuelles
        # envoyée à J-15 puis J-40
        user = baker.make("users.User", is_valid=True)
        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=15),
        )
        saved_search_2 = baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # QUAND je récupère les notifications mensuelles à envoyer
        notifications = get_saved_search_notifications_to_send()

        # ALORS je récupère la seconde notification envoyée à J-40
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].id, saved_search_2.id)

    def test_get_two_weeks_saved_searches(self):
        # ÉTANT DONNÉ un utilisateur avec deux notifications toutes les deux semaines
        # envoyée à J-10 puis J-20
        user = baker.make("users.User", is_valid=True)

        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.TWO_WEEKS,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=10),
        )
        saved_search_2 = baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.TWO_WEEKS,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=20),
        )

        # QUAND je récupère les notifications mensuelles à envoyer
        notifications = get_saved_search_notifications_to_send()

        # ALORS je récupère la seconde notification à envoyer à J-20
        self.assertEqual(len(notifications), 1)
        self.assertEqual(notifications[0].id, saved_search_2.id)

    def test_get_two_weeks_no_saved_searches(self):
        # ÉTANT DONNÉ un utilisateur avec deux notifications mensuelles
        # envoyée à J-5 puis J-10
        user = baker.make("users.User", is_valid=True)

        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.TWO_WEEKS,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=5),
        )
        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.TWO_WEEKS,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=10),
        )

        # QUAND je récupère les notifications à envoyer tous les 15 jours
        notifications = get_saved_search_notifications_to_send()

        # ALORS je ne récupère aucune notification
        self.assertEqual(len(notifications), 0)

    def test_get_monthly_no_saved_searches(self):
        # ÉTANT DONNÉ un utilisateur avec deux notifications mensuelles
        # envoyée à J-15 puis J-20
        user = baker.make("users.User", is_valid=True)

        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=15),
        )
        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=20),
        )

        # QUAND je récupère les notifications mensuelles à envoyer
        notifications = get_saved_search_notifications_to_send()

        # ALORS je ne récupère aucune notification
        self.assertEqual(len(notifications), 0)

    def test_get_create_notification_location_only(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle envoyée à J-40
        user = baker.make("users.User", is_valid=True)
        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # ET un service mis à jour à J-20
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)

    def test_get_no_notification_location(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle envoyée à J-40
        user = baker.make("users.User", is_valid=True)
        baker.make(
            "SavedSearch",
            user=user,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # ET un service mis à jour à J-60
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=60),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS je n'ai pas d'email
        self.assertEqual(len(mail.outbox), 0)

    def test_get_create_notification_with_category(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        user = baker.make("users.User", is_valid=True)
        cat1 = baker.make("ServiceCategory", value="cat1", label="cat1")

        baker.make(
            "SavedSearch",
            user=user,
            category=cat1,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # ET un service mis à jour à J-20 lié à la même catégorie
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn("pour la thématique &quot;cat1", mail.outbox[0].body)
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)

    def test_get_create_notification_with_category_and_subcategories(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie et deux sous-catégories
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        sub_category = baker.make(
            "ServiceSubCategory", value="cat1--sub1", label="cat1--sub1"
        )
        sub_category_2 = baker.make(
            "ServiceSubCategory", value="cat1--sub2", label="cat1--sub2"
        )

        savedSearch = baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )
        savedSearch.subcategories.set([sub_category, sub_category_2])

        # ET un service mis à jour à J-20 lié à la même catégorie et sous-catégories
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            subcategories="cat1--sub1,cat1--sub2",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn("pour la thématique &quot;cat1", mail.outbox[0].body)
        self.assertIn(
            "pour le(s) besoin(s) : cat1--sub1, cat1--sub2", mail.outbox[0].body
        )
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)

    def test_get_create_notification_with_category_and_subcategories_and_kinds(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        sub_category = baker.make(
            "ServiceSubCategory", value="cat1--sub1", label="cat1--sub1"
        )
        sub_category_2 = baker.make(
            "ServiceSubCategory", value="cat1--sub2", label="cat1--sub2"
        )
        kind = baker.make("ServiceKind", value="kind1", label="kind1")
        kind_2 = baker.make("ServiceKind", value="kind2", label="kind2")

        savedSearch = baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )
        savedSearch.subcategories.set([sub_category, sub_category_2])
        savedSearch.kinds.set([kind, kind_2])

        # ET un service mis à jour à J-20 lié à la même catégorie, sous-catégories et types de service
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            subcategories="cat1--sub1,cat1--sub2",
            kinds=[kind, kind_2],
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn("pour la thématique &quot;cat1", mail.outbox[0].body)
        self.assertIn(
            "pour le(s) besoin(s) : cat1--sub1, cat1--sub2", mail.outbox[0].body
        )
        self.assertIn(
            "pour le(s) type(s) de service : kind1, kind2", mail.outbox[0].body
        )
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)

    def test_get_create_notification_with_category_and_subcategories_and_kinds_and_fee(
        self,
    ):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services et un frais à charge
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        sub_category = baker.make(
            "ServiceSubCategory", value="cat1--sub1", label="cat1--sub1"
        )
        sub_category_2 = baker.make(
            "ServiceSubCategory", value="cat1--sub2", label="cat1--sub2"
        )
        kind = baker.make("ServiceKind", value="kind1", label="kind1")
        kind_2 = baker.make("ServiceKind", value="kind2", label="kind2")
        fee = baker.make("ServiceFee", value="fee", label="fee")

        savedSearch = baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )
        savedSearch.subcategories.set([sub_category, sub_category_2])
        savedSearch.kinds.set([kind, kind_2])
        savedSearch.fees.set([fee])

        # ET un service mis à jour à J-20 lié à la même catégorie, sous-catégories, types de service et frais à charge
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            subcategories="cat1--sub1,cat1--sub2",
            kinds=[kind, kind_2],
            fee_condition=fee,
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn("pour la thématique &quot;cat1", mail.outbox[0].body)
        self.assertIn(
            "pour le(s) besoin(s) : cat1--sub1, cat1--sub2", mail.outbox[0].body
        )
        self.assertIn(
            "pour le(s) type(s) de service : kind1, kind2", mail.outbox[0].body
        )
        self.assertIn("avec comme frais à charge : fee", mail.outbox[0].body)
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)

    def test_get_create_notification_with_two_services(self):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services et un frais à charge
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")

        baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # ET deux services mis à jour à J-20 liés à la même catégorie mais avec un seul service modifié récemment
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )
        make_service(
            name="service_2",
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=80),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS j'ai un e-mail
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(
            mail.outbox[0].subject,
            "Il y a de nouveaux services correspondant à votre alerte",
        )
        self.assertIn(f"<strong>{self.service_name}</strong>", mail.outbox[0].body)
        self.assertNotIn("<strong>service_2</strong>", mail.outbox[0].body)

    def test_get_create_notification_with_invalid_fee(
        self,
    ):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services et un frais à charge
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        fee1 = baker.make("ServiceFee", value="fee1", label="fee1")
        fee2 = baker.make("ServiceFee", value="fee2", label="fee2")

        savedSearch = baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )
        savedSearch.fees.set([fee1])

        # ET un service mis à jour à J-20 lié à la même catégorie, sous-catégories, types de service et frais à charge
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            fee_condition=fee2,
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS je n'ai pas d'email
        self.assertEqual(len(mail.outbox), 0)

    def test_get_create_notification_with_invalid_category(
        self,
    ):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services et un frais à charge
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        baker.make("ServiceCategory", value="cat2", label="cat2")

        baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )

        # ET un service mis à jour à J-20 lié à la même catégorie, sous-catégories, types de service et frais à charge
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat2",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS je n'ai pas d'email
        self.assertEqual(len(mail.outbox), 0)

    def test_get_create_notification_with_invalid_subcategory(
        self,
    ):
        # ÉTANT DONNÉ un utilisateur avec une notification mensuelle à J-40 lié à une catégorie
        # et deux sous-catégories et deux types de services et un frais à charge
        user = baker.make("users.User", is_valid=True)
        category = baker.make("ServiceCategory", value="cat1", label="cat1")
        sub_category_1 = baker.make(
            "ServiceSubCategory", value="cat1--sub1", label="cat1--sub1"
        )
        baker.make("ServiceSubCategory", value="cat1--sub2", label="cat1--sub2")

        savedSearch = baker.make(
            "SavedSearch",
            user=user,
            category=category,
            frequency=SavedSearchFrequency.MONTHLY,
            city_label=SAVE_SEARCH_ARGS.get("city_label"),
            city_code=SAVE_SEARCH_ARGS.get("city_code"),
            last_notification_date=timezone.now() - timedelta(days=40),
        )
        savedSearch.subcategories.set([sub_category_1])

        # ET un service mis à jour à J-20 lié à la même catégorie, sous-catégories, types de service et frais à charge
        make_service(
            name=self.service_name,
            status=ServiceStatus.PUBLISHED,
            categories="cat1",
            subcategories="cat1--sub2",
            diffusion_zone_type=AdminDivisionType.CITY,
            publication_date=timezone.now() - timedelta(days=20),
            diffusion_zone_details=SAVE_SEARCH_ARGS.get("city_code"),
        )

        # QUAND j'envoie les notifications
        self.call_command()

        # ALORS je n'ai pas d'email
        self.assertEqual(len(mail.outbox), 0)
