from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import make_service, make_structure
from dora.services.enums import ServiceStatus


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

    def test_coord_can_see_structures_in_his_dept(self):
        structure = make_structure(department=31)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data[0]["slug"], structure.slug)

    def test_coord_cant_see_structures_outside_his_dept(self):
        make_structure(department=12)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_coord_without_dept_cant_see_structures(self):
        manager = baker.make(
            "users.User", is_valid=True, is_staff=False, is_manager=True
        )
        make_structure(department=31)
        self.client.force_authenticate(user=manager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 403)

    def test_coord_can_see_specific_structure_in_his_dept(self):
        structure = make_structure(department=31)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure.slug)

    def test_coord_cant_see_specific_structure_outside_his_dept(self):
        structure = make_structure(department=12)
        self.client.force_authenticate(user=self.manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 404)

    def test_coord_without_dept_cant_see_specific_structure(self):
        manager = baker.make(
            "users.User", is_valid=True, is_staff=False, is_manager=True
        )
        structure = make_structure(department=31)
        self.client.force_authenticate(user=manager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 403)

    ## Plusieurs départements
    def test_bicoord_can_see_structures_in_his_depts(self):
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

    def test_bicoord_cant_see_structures_outside_his_depts(self):
        make_structure(department="12")
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get("/structures-admin/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_bicoord_can_see_specific_structures_in_his_depts(self):
        structure1 = make_structure(department="31")
        structure2 = make_structure(department="08")
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get(f"/structures-admin/{structure1.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure1.slug)
        response = self.client.get(f"/structures-admin/{structure2.slug}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["slug"], structure2.slug)

    def test_bicoord_cant_see_specific_structure_outside_his_depts(self):
        structure = make_structure(department=12)
        self.client.force_authenticate(user=self.bimanager)
        response = self.client.get(f"/structures-admin/{structure.slug}/")
        self.assertEqual(response.status_code, 404)
