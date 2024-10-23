from datetime import timedelta

from django.utils.timezone import now
from model_bakery import baker
from rest_framework.test import APITestCase

from dora.core.test_utils import (
    make_published_service,
    make_service,
    make_structure,
    make_user,
)

from ..enums import ServiceStatus
from ..models import Bookmark


class ServiceBookmarkTestCase(APITestCase):
    def test_add_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        service = make_published_service()

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bookmark.objects.count(), 1)

        bookmark = Bookmark.objects.get(service=service)
        self.assertEqual(bookmark.user, user)
        self.assertEqual(bookmark.di_id, "")
        self.assertTrue(now() - bookmark.creation_date < timedelta(seconds=2))

    def test_add_di_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/bookmarks/", {"slug": "di_source--123456789", "is_di": True}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bookmark.objects.count(), 1)

        di_bookmark = Bookmark.objects.get(di_id="di_source--123456789")
        self.assertEqual(di_bookmark.user, user)
        self.assertEqual(di_bookmark.service_id, None)
        self.assertTrue(now() - di_bookmark.creation_date < timedelta(seconds=2))

    def test_add_duplicate_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        service = make_published_service()

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bookmark.objects.count(), 1)
        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertContains(response, "ce bookmark existe déjà", status_code=400)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_add_duplicate_di_bookmark(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/bookmarks/", {"slug": "di_source--123456789", "is_di": True}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.post(
            "/bookmarks/", {"slug": "di_source--123456789", "is_di": True}
        )
        self.assertEqual(response.status_code, 400)
        self.assertContains(response, "ce bookmark existe déjà", status_code=400)

        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_add_bookmark_anonymous(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        service = make_published_service()

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_cant_add_di_bookmark_anonymous(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        response = self.client.post("/bookmarks/", {"di_id": "di_source--123456789"})
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_cant_add_bookmark_draft(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        service = make_service(status=ServiceStatus.DRAFT)

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_can_add_bookmark_my_drafts(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        structure = make_structure(user=user)
        service = make_service(structure=structure, status=ServiceStatus.DRAFT)
        self.client.force_authenticate(user=user)

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 201)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_add_bookmark_archived(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        service = make_service(status=ServiceStatus.ARCHIVED)

        response = self.client.post("/bookmarks/", {"slug": service.slug})
        self.assertEqual(response.status_code, 403)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_can_remove_bookmark(self):
        user = make_user()
        self.client.force_authenticate(user=user)
        bookmark = baker.make(
            "services.Bookmark", service=make_published_service(), user=user
        )
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_can_remove_di_bookmark(self):
        user = make_user()
        self.client.force_authenticate(user=user)
        bookmark = baker.make(
            "services.Bookmark", di_id="di_source--123456789", user=user
        )
        self.assertEqual(Bookmark.objects.count(), 1)
        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 204)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_cant_remove_somebody_else_bookmark(self):
        user = make_user()
        self.client.force_authenticate(user=user)
        bookmark = baker.make("services.Bookmark", service=make_published_service())
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_remove_somebody_else_di_bookmark(self):
        user = make_user()
        self.client.force_authenticate(user=user)
        bookmark = baker.make("services.Bookmark", di_id="di_source--123456789")
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_remove_bookmark_anonymous(self):
        bookmark = baker.make("services.Bookmark", service=make_published_service())
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_remove_di_bookmark_anonymous(self):
        bookmark = baker.make("services.Bookmark", di_id="di_source--123456789")
        self.assertEqual(Bookmark.objects.count(), 1)

        response = self.client.delete(f"/bookmarks/{bookmark.id}/")
        self.assertEqual(response.status_code, 401)
        self.assertEqual(Bookmark.objects.count(), 1)

    def test_cant_add_bookmark_incorrect_slug(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)

        response = self.client.post("/bookmarks/", {"slug": "abcd"})
        self.assertEqual(response.status_code, 404)
        self.assertEqual(Bookmark.objects.count(), 0)

    def test_list_bookmarks_show_my_bookmarks(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        baker.make("services.Bookmark", service=make_published_service(), user=user)
        baker.make("services.Bookmark", service=make_published_service(), user=user)
        baker.make("services.Bookmark", di_id="di_source--123456789", user=user)

        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 3)
        # Les services data·inclusion ne sont pas mockés pour l'instant
        self.assertTrue(
            "name" in response.data[0]["service"]
            or "name" in response.data[1]["service"]
        )

    def test_list_bookmarks_dont_show_others_bookmarks(self):
        user = make_user()
        self.client.force_authenticate(user=user)
        baker.make("services.Bookmark", service=make_published_service())
        baker.make("services.Bookmark", service=make_published_service())
        baker.make("services.Bookmark", di_id="di_source--123456789")

        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 0)

    def test_cant_list_bookmarks_anonymous(self):
        baker.make("services.Bookmark", service=make_published_service())
        baker.make("services.Bookmark", service=make_published_service())
        baker.make("services.Bookmark", di_id="di_source--123456789")

        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 401)

    def test_list_bookmarks_filters_unaccessible_services(self):
        self.assertEqual(Bookmark.objects.count(), 0)
        user = make_user()
        self.client.force_authenticate(user=user)
        baker.make("services.Bookmark", service=make_published_service(), user=user)
        baker.make(
            "services.Bookmark",
            service=make_service(status=ServiceStatus.DRAFT),
            user=user,
        )
        baker.make(
            "services.Bookmark",
            service=make_service(status=ServiceStatus.ARCHIVED),
            user=user,
        )
        baker.make("services.Bookmark", di_id="di_source--123456789", user=user)
        response = self.client.get("/bookmarks/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)
