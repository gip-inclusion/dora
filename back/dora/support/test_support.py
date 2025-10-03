from dateutil.relativedelta import relativedelta
from django.utils import timezone
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.models import ModerationStatus
from dora.core.test_utils import make_service, make_structure, make_user
from dora.services.enums import ServiceStatus
from dora.services.models import UpdateFrequency
from dora.structures.models import StructureMember, StructurePutativeMember


class SupportTestCase(APITestCase):
    def setUp(self):
        self.staff = baker.make("users.User", is_valid=True, is_staff=True)
        self.nonstaff = baker.make("users.User", is_valid=True, is_staff=False)

    def test_staff_can_see_service_list(self):
        service = make_service(status=ServiceStatus.PUBLISHED)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get("/services-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], service.slug)

    def test_staff_can_see_service(self):
        service = make_service(status=ServiceStatus.PUBLISHED)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f"/services-admin/{service.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], service.slug)

    def test_nonstaff_cant_see_service_list(self):
        make_service(status=ServiceStatus.PUBLISHED)
        self.client.force_authenticate(user=self.nonstaff)
        response = self.client.get("/services-admin/")
        self.assertEqual(response.status_code, 403)

    def test_nonstaff_cant_see_service(self):
        service = make_service(status=ServiceStatus.PUBLISHED)
        self.client.force_authenticate(user=self.nonstaff)
        response = self.client.get(f"/services-admin/{service.slug}/")
        self.assertEqual(response.status_code, 403)

    def test_anon_cant_see_service_list(self):
        make_service(status=ServiceStatus.PUBLISHED)
        response = self.client.get("/services-admin/")
        self.assertEqual(response.status_code, 401)

    def test_anon_cant_see_service(self):
        service = make_service(status=ServiceStatus.PUBLISHED)
        response = self.client.get(f"/services-admin/{service.slug}/")
        self.assertEqual(response.status_code, 401)

    def test_staff_cant_see_drafts(self):
        service = make_service(status=ServiceStatus.DRAFT)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f"/services-admin/{service.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_staff_cant_see_archive(self):
        service = make_service(status=ServiceStatus.ARCHIVED)
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f"/services-admin/{service.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_staff_can_see_structure_list(self):
        structure = make_structure()
        self.client.force_authenticate(user=self.staff)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], structure.slug)

    def test_staff_can_see_structure(self):
        structure = make_structure()
        self.client.force_authenticate(user=self.staff)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure.slug)

    def test_nonstaff_cant_see_structure_list(self):
        make_structure()
        self.client.force_authenticate(user=self.nonstaff)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 403)

    def test_nonstaff_cant_see_structure(self):
        structure = make_structure()
        self.client.force_authenticate(user=self.nonstaff)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 403)

    def test_anon_cant_see_structure_list(self):
        make_structure()
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 401)

    def test_anon_cant_see_structure(self):
        structure = make_structure()
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 401)


def make_service_in_dept(dept, **kwargs):
    structure = make_structure(department=dept)
    return make_service(structure=structure, status=ServiceStatus.PUBLISHED)


class ManagerTestCase(APITestCase):
    def setUp(self):
        self.manager = baker.make(
            "users.User",
            is_valid=True,
            is_staff=False,
            is_manager=True,
            departments=[31],
        )

        self.bimanager = baker.make(
            "users.User",
            is_valid=True,
            is_staff=False,
            is_manager=True,
            departments=["31", "08"],
        )

    def test_manager_can_see_structures_in_his_dept(self):
        structure = make_structure(department=31)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], structure.slug)

    def test_manager_cant_see_structures_outside_his_dept(self):
        make_structure(department=12)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_manager_without_dept_cant_see_structures(self):
        manager = baker.make(
            "users.User", is_valid=True, is_staff=False, is_manager=True
        )
        make_structure(department=31)
        self.client.force_authenticate(user=manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 403)

    def test_manager_can_see_specific_structure_in_his_dept(self):
        structure = make_structure(department=31)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure.slug)

    def test_manager_cant_see_specific_structure_outside_his_dept(self):
        structure = make_structure(department=12)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_manager_without_dept_cant_see_specific_structure(self):
        manager = baker.make(
            "users.User", is_valid=True, is_staff=False, is_manager=True
        )
        structure = make_structure(department=31)
        self.client.force_authenticate(user=manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 403)

    def test_manager_can_see_if_structure_is_orphan(self):
        manager = make_user(
            is_valid=True, is_staff=False, is_manager=True, departments=[31]
        )
        structure = make_structure(department=31, user=None, putative_member=None)
        self.client.force_authenticate(user=manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["is_orphan"])

    def test_manager_can_see_if_structure_is_awaiting_moderation(self):
        manager = make_user(
            is_valid=True, is_staff=False, is_manager=True, departments=[31]
        )
        structure = make_structure(
            department=31, moderation_status=ModerationStatus.NEED_NEW_MODERATION
        )
        self.client.force_authenticate(user=manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.data["awaiting_moderation"])

    ## Plusieurs départements
    def test_manager_can_see_structures_in_his_depts(self):
        structure1 = make_structure(department="31")
        structure2 = make_structure(department="08")
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            response.data[0]["slug"] == structure1.slug
            or response.data[0]["slug"] == structure2.slug
        )
        self.assertTrue(
            response.data[1]["slug"] == structure1.slug
            or response.data[1]["slug"] == structure2.slug
        )

    def test_manager_cant_see_structures_outside_his_depts(self):
        make_structure(department="12")
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_manager_can_see_specific_structures_in_his_depts(self):
        structure1 = make_structure(department="31")
        structure2 = make_structure(department="08")
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get(f"/structures-admin/{structure1.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure1.slug)
        response = self.client.get(f"/structures-admin/{structure2.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure2.slug)

    def test_manager_cant_see_specific_structure_outside_his_depts(self):
        structure = make_structure(department=12)
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 404)


class StructureAdminTestCase(APITestCase):
    def setUp(self):
        self.admin = baker.make(
            "users.User",
            is_staff=True,
        )

    def test_num_queries_structures_admin_list(self):
        make_structure()
        make_structure()
        make_structure()
        make_structure()
        self.client.force_authenticate(user=make_user(is_staff=True))

        with self.assertNumQueries(3):
            self.client.get("/structures-admin/")

    def test_num_queries_structures_admin_detail(self):
        structure = make_structure()
        self.client.force_authenticate(user=make_user(is_staff=True))

        with self.assertNumQueries(9):
            self.client.get(f"/structures-admin/{structure.slug}/")

    def test_structures_admin_list_basic_fields(self):
        structure = make_structure(department="31")

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 1)

        data = response.data[0]
        self.assertEqual(data["name"], structure.name)
        self.assertEqual(data["department"], structure.department)
        self.assertEqual(data["slug"], structure.slug)

        basic_fields = [
            "department",
            "name",
            "siret",
            "slug",
            "typology",
            "typology_display",
            "latitude",
            "longitude",
            "categories",
            "national_labels",
        ]
        for field in basic_fields:
            self.assertIn(field, data, f"Basic field '{field}' missing from response")

    def test_structures_admin_list_service_counts(self):
        structure = make_structure(department="31")

        make_service(structure=structure, status=ServiceStatus.PUBLISHED)
        make_service(structure=structure, status=ServiceStatus.DRAFT)
        make_service(structure=structure, status=ServiceStatus.ARCHIVED)

        make_service(
            structure=structure,
            status=ServiceStatus.PUBLISHED,
            update_frequency=UpdateFrequency.EVERY_MONTH,
            modification_date=timezone.now() - relativedelta(months=2),
        )

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)
        data = response.data[0]

        self.assertEqual(data["num_published_services"], 2)
        self.assertEqual(data["num_draft_services"], 1)
        self.assertEqual(data["num_services"], 3)
        self.assertEqual(data["num_outdated_services"], 1)

    def test_structures_admin_list_orphan_status(self):
        orphan_structure = make_structure(department="31")
        # La structure est une orphéline parce qu'il n'y a pas de membre

        non_orphan_structure = make_structure(department="31")
        StructureMember.objects.create(
            structure=non_orphan_structure,
            user=make_user(is_valid=True, is_active=True),
            is_admin=True,
        )

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

        orphan_data = next(
            s for s in response.data if s["slug"] == orphan_structure.slug
        )
        non_orphan_data = next(
            s for s in response.data if s["slug"] == non_orphan_structure.slug
        )

        self.assertTrue(orphan_data["is_orphan"])
        self.assertFalse(non_orphan_data["is_orphan"])

    def test_structures_admin_list_waiting_status(self):
        waiting_structure = make_structure(department="31")
        StructurePutativeMember.objects.create(
            structure=waiting_structure,
            user=make_user(is_valid=True, is_active=True),
            is_admin=True,
            invited_by_admin=True,
        )

        non_waiting_structure = make_structure(department="31")
        StructureMember.objects.create(
            structure=non_waiting_structure,
            user=make_user(is_valid=True, is_active=True),
            is_admin=True,
        )

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)

        waiting_data = next(
            s for s in response.data if s["slug"] == waiting_structure.slug
        )
        non_waiting_data = next(
            s for s in response.data if s["slug"] == non_waiting_structure.slug
        )

        self.assertTrue(waiting_data["is_waiting"])
        self.assertFalse(non_waiting_data["is_waiting"])

    def test_structures_admin_list_moderation_status(self):
        moderation_structure = make_structure(
            department="31", moderation_status=ModerationStatus.NEED_NEW_MODERATION
        )

        validated_structure = make_structure(
            department="31", moderation_status=ModerationStatus.VALIDATED
        )

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)

        moderation_data = next(
            s for s in response.data if s["slug"] == moderation_structure.slug
        )
        validated_data = next(
            s for s in response.data if s["slug"] == validated_structure.slug
        )

        self.assertTrue(moderation_data["awaiting_moderation"])
        self.assertFalse(validated_data["awaiting_moderation"])

    def test_structures_admin_list_activation_status(self):
        structure_without_services = make_structure(department="31")
        draft_only_structure = make_structure(department="31")
        # Les structures sans services et en brouillon ont besoin de l'activation

        make_service(structure=draft_only_structure, status=ServiceStatus.DRAFT)

        activated_structure = make_structure(department="31")
        make_service(structure=activated_structure, status=ServiceStatus.PUBLISHED)

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)

        structure_without_services_data = next(
            s for s in response.data if s["slug"] == structure_without_services.slug
        )
        draft_only_data = next(
            s for s in response.data if s["slug"] == draft_only_structure.slug
        )
        activated_data = next(
            s for s in response.data if s["slug"] == activated_structure.slug
        )

        self.assertTrue(structure_without_services_data["awaiting_activation"])
        self.assertTrue(draft_only_data["awaiting_activation"])
        self.assertFalse(activated_data["awaiting_activation"])

    def test_structures_admin_list_update_status(self):
        structure_needing_update = make_structure(department="31")
        make_service(
            structure=structure_needing_update,
            status=ServiceStatus.PUBLISHED,
            update_frequency=UpdateFrequency.EVERY_MONTH,
            modification_date=timezone.now() - relativedelta(months=2),
        )

        up_to_date_structure = make_structure(department="31")
        make_service(
            structure=up_to_date_structure,
            status=ServiceStatus.PUBLISHED,
            update_frequency=UpdateFrequency.EVERY_MONTH,
            modification_date=timezone.now(),
        )

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)

        update_data = next(
            s for s in response.data if s["slug"] == structure_needing_update.slug
        )
        current_data = next(
            s for s in response.data if s["slug"] == up_to_date_structure.slug
        )

        self.assertTrue(update_data["awaiting_update"])
        self.assertFalse(current_data["awaiting_update"])

    def test_structures_admin_list_obsolete_status(self):
        obsolete_structure = make_structure(department="31", is_obsolete=True)
        normal_structure = make_structure(department="31", is_obsolete=False)

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)

        obsolete_data = next(
            s for s in response.data if s["slug"] == obsolete_structure.slug
        )
        normal_data = next(
            s for s in response.data if s["slug"] == normal_structure.slug
        )

        self.assertTrue(obsolete_data["is_obsolete"])
        self.assertFalse(normal_data["is_obsolete"])

    def test_structures_admin_list_required_fields_present(self):
        make_structure(department="31")

        self.client.force_authenticate(user=make_user(is_staff=True))

        response = self.client.get("/structures-admin/?department=31")

        self.assertEqual(response.status_code, 200)
        data = response.data[0]

        required_fields = [
            "awaiting_moderation",
            "awaiting_activation",
            "awaiting_update",
            "categories",
            "department",
            "is_obsolete",
            "is_orphan",
            "is_waiting",
            "latitude",
            "longitude",
            "name",
            "national_labels",
            "num_draft_services",
            "num_outdated_services",
            "num_published_services",
            "num_services",
            "siret",
            "slug",
            "typology",
            "typology_display",
        ]

        for field in required_fields:
            self.assertIn(
                field, data, f"Required field '{field}' missing from list response"
            )

        self.assertIsInstance(data["categories"], list)
