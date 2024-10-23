from datetime import timedelta
from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time
from rest_framework.test import APITestCase

from dora.core.test_utils import make_service, make_structure, make_user
from dora.services.enums import ServiceStatus


class ServicesNotificationsTestCase(APITestCase):
    def setUp(self):
        self.structure = make_structure()

    def call_command(self):
        call_command("send_services_reminders", stdout=StringIO())

    ########
    # Drafts
    ########

    def test_old_drafts_creator_notified(self):
        with freeze_time(timezone.now() - timedelta(days=8)):
            service = make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Des mises à jour de votre offre de service sur DORA sont nécessaires",
            mail.outbox[0].subject,
        )
        self.assertIn(service.structure.slug, mail.outbox[0].body)
        self.assertIn("/auth/connexion?next", mail.outbox[0].body)
        self.assertIn("services%3Fservice-status%3DDRAFT", mail.outbox[0].body)
        self.assertIn(service.creator.email, mail.outbox[0].to)

    def test_draft_newer_than_7_days_not_notified(self):
        with freeze_time(timezone.now() - timedelta(days=6)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)

    def test_old_drafts_creator_editor_notified(self):
        with freeze_time(timezone.now() - timedelta(days=8)):
            service = make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
                last_editor=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(service.creator.email, [*mail.outbox[0].to, *mail.outbox[1].to])
        self.assertIn(
            service.last_editor.email, [*mail.outbox[0].to, *mail.outbox[1].to]
        )

    def test_old_drafts_same_creator_editor_notified_once(self):
        creator = make_user(self.structure)
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=creator,
                last_editor=creator,
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)

    def test_notdraft_older_than_7_days_not_notified(self):
        with freeze_time(timezone.now() - timedelta(days=8)):
            service = make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
        with freeze_time(timezone.now() - timedelta(days=4)):
            service.status = ServiceStatus.PUBLISHED
            service.save()
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)

    def test_old_drafts_admin_notified(self):
        admin = make_user(self.structure, is_admin=True)
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(admin.email, [*mail.outbox[0].to, *mail.outbox[1].to])

    def test_old_drafts_editors_notified(self):
        editor = make_user(self.structure)
        with freeze_time(timezone.now() - timedelta(days=8)):
            service = make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
            self.client.force_authenticate(user=editor)
            response = self.client.patch(f"/services/{service.slug}/", {"name": "xxx"})
            self.assertEqual(response.status_code, 200)
        self.call_command()
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(editor.email, [*mail.outbox[0].to, *mail.outbox[1].to])

    def test_old_drafts_admin_other_struct_not_notified(self):
        admin = make_user(is_admin=True)
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn(admin.email, mail.outbox[0].to)

    def test_old_drafts_user_in_charge_notified_if_member(self):
        user_in_charge = make_user(self.structure)
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
                contact_email=user_in_charge.email,
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 2)
        self.assertIn(user_in_charge.email, [*mail.outbox[0].to, *mail.outbox[1].to])

    def test_old_drafts_user_in_charge_not_notified_if_not_member(self):
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(self.structure),
                contact_email="test@exemple.com",
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)
        self.assertNotIn("test@exemple.com", mail.outbox[0].to)

    def test_old_draft_people_outside_struct_not_notified(self):
        with freeze_time(timezone.now() - timedelta(days=8)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=make_user(),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)

    def test_old_drafts_user_notified_once_a_month_max(self):
        user = make_user(self.structure)
        with freeze_time(timezone.now() - timedelta(days=70)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.DRAFT,
                creator=user,
            )
        with freeze_time(timezone.now() - timedelta(days=60)):
            # notification envoyée quand le brouillon est assez vieux
            self.call_command()
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn(user.email, mail.outbox[0].to)
            mail.outbox = []

        with freeze_time(timezone.now() - timedelta(days=50)):
            # on ne renvoie pas de notification à l'utilisateur trop souvent
            self.call_command()
            self.assertEqual(len(mail.outbox), 0)

        with freeze_time(timezone.now() - timedelta(days=29)):
            # mais on renvoie une notif quand un delai suffisant est passé
            self.call_command()
            self.assertEqual(len(mail.outbox), 1)
            self.assertIn(user.email, mail.outbox[0].to)

    ##########################
    # Services à mettre à jour
    ##########################

    def test_service_more_than_6_months_notified(self):
        with freeze_time(timezone.now() - timedelta(days=7 * 30)):
            service = make_service(
                structure=self.structure,
                status=ServiceStatus.PUBLISHED,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn(
            "Des mises à jour de votre offre de service sur DORA sont nécessaires",
            mail.outbox[0].subject,
        )
        self.assertIn(service.structure.slug, mail.outbox[0].body)
        self.assertIn("/auth/connexion?next", mail.outbox[0].body)
        self.assertIn("services%3Fupdate-status%3DALL", mail.outbox[0].body)
        self.assertIn(service.creator.email, mail.outbox[0].to)

    def test_service_less_than_6_months__not_notified(self):
        with freeze_time(timezone.now() - timedelta(days=5 * 30)):
            make_service(
                structure=self.structure,
                status=ServiceStatus.PUBLISHED,
                creator=make_user(self.structure),
            )
        self.call_command()
        self.assertEqual(len(mail.outbox), 0)
