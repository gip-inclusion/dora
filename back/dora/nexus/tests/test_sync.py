import json

from django.utils import timezone

from dora.core.test_utils import make_structure, make_structure_member, make_user
from dora.structures.models import Structure, StructureMember
from dora.users.models import User


def assert_call_content(call, expected_data):
    # the order doesn't matter
    data = json.loads(call.request.content.decode())
    assert sorted(data, key=lambda d: d["id"]) == sorted(
        expected_data, key=lambda d: d["id"]
    )


def make_syncable_user(**kwargs):
    return make_user(first_name="John", last_name="Doe", **kwargs)


def make_syncable_member(**kwargs):
    user = make_syncable_user()
    return make_structure_member(user=user, **kwargs)


class TestUserSync:
    def test_sync_on_model_save_new_instance(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        with django_capture_on_commit_callbacks(execute=True):
            user = make_syncable_user()

        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {
                    "id": str(user.pk),
                    "kind": user.main_activity,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": user.email,
                    "phone": "",
                    "last_login": None,
                    "auth": "MAGIC_LINK",
                },
            ],
        )

    def test_sync_on_model_save_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            user.email = "another@email.com"
            user.last_login = timezone.now()
            user.save()
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {
                    "id": str(user.pk),
                    "kind": user.main_activity,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "email": "another@email.com",
                    "phone": "",
                    "last_login": user.last_login.isoformat(),
                    "auth": "MAGIC_LINK",
                },
            ],
        )

    def test_no_sync_on_model_save_no_changed_data(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            user.save()
        assert mock_nexus_api.calls == []

    def test_no_sync_on_model_save_non_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            user.partner_kind = "AUTRE"
            user.save()
        assert mock_nexus_api.calls == []

    def test_delete_on_model_save(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        with django_capture_on_commit_callbacks(execute=True):
            user_1 = make_syncable_user(is_active=False)
            user_2 = make_syncable_user(is_staff=True)

        [call_1, call_2] = mock_nexus_api.calls
        assert call_1.request.method == "DELETE"
        assert call_1.request.url == "http://nexus/api/users"
        assert_call_content(call_1, [{"id": str(user_1.pk)}])
        assert call_2.request.method == "DELETE"
        assert call_2.request.url == "http://nexus/api/users"
        assert_call_content(call_2, [{"id": str(user_2.pk)}])

    def test_delete_on_model_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user = make_syncable_user()
        user_id = user.pk

        with django_capture_on_commit_callbacks(execute=True):
            user.delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(call, [{"id": str(user_id)}])

    def test_sync_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user_1 = make_syncable_user()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            User.objects.filter(pk__in=[user_1.pk, user_2.pk]).order_by("pk").update(
                first_name="John"
            )
        print(mock_nexus_api.calls)
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {
                    "id": str(user_1.pk),
                    "kind": user_1.main_activity,
                    "first_name": "John",
                    "last_name": user_1.last_name,
                    "email": user_1.email,
                    "phone": "",
                    "last_login": None,
                    "auth": "MAGIC_LINK",
                },
                {
                    "id": str(user_2.pk),
                    "kind": user_2.main_activity,
                    "first_name": "John",
                    "last_name": user_2.last_name,
                    "email": user_2.email,
                    "phone": "",
                    "last_login": None,
                    "auth": "MAGIC_LINK",
                },
            ],
        )

    def test_delete_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user_1 = make_syncable_user()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            User.objects.filter(pk__in=[user_1.pk, user_2.pk]).order_by("pk").update(
                is_active=False
            )
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {"id": str(user_1.pk)},
                {"id": str(user_2.pk)},
            ],
        )

    def test_delete_on_manager_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user_1 = make_syncable_user()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            User.objects.filter(pk__in=[user_1.pk, user_2.pk]).order_by("pk").delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {"id": str(user_1.pk)},
                {"id": str(user_2.pk)},
            ],
        )

    def test_sync_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user_1 = make_syncable_user()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            user_1.first_name = "John"
            user_2.first_name = "Not John"
            User.objects.filter(pk__in=[user_1.pk, user_2.pk]).bulk_update(
                [user_1, user_2], ["first_name"]
            )
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {
                    "id": str(user_1.pk),
                    "kind": user_1.main_activity,
                    "first_name": "John",
                    "last_name": user_1.last_name,
                    "email": user_1.email,
                    "phone": "",
                    "last_login": None,
                    "auth": "MAGIC_LINK",
                },
                {
                    "id": str(user_2.pk),
                    "kind": user_2.main_activity,
                    "first_name": "Not John",
                    "last_name": user_2.last_name,
                    "email": user_2.email,
                    "phone": "",
                    "last_login": None,
                    "auth": "MAGIC_LINK",
                },
            ],
        )

    def test_delete_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user_1 = make_syncable_user()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            user_1.is_active = False
            user_2.is_active = False
            User.objects.filter(pk__in=[user_1.pk, user_2.pk]).bulk_update(
                [user_1, user_2], ["is_active"]
            )
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/users"
        assert_call_content(
            call,
            [
                {"id": str(user_1.pk)},
                {"id": str(user_2.pk)},
            ],
        )


class TestStructureSync:
    def test_sync_on_model_save_new_instance(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        with django_capture_on_commit_callbacks(execute=True):
            structure = make_structure()

        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {
                    "id": str(structure.pk),
                    "kind": structure.typology,
                    "siret": structure.siret,
                    "name": structure.name,
                    "phone": structure.phone,
                    "email": structure.email,
                    "address_line_1": structure.address1,
                    "address_line_2": "",
                    "post_code": structure.postal_code,
                    "city": structure.city,
                    "department": structure.department,
                    "website": structure.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure.full_desc,
                    "source_link": structure.get_absolute_url(),
                },
            ],
        )

    def test_sync_on_model_save_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            structure.email = "another@email.com"
            structure.save()
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {
                    "id": str(structure.pk),
                    "kind": structure.typology,
                    "siret": structure.siret,
                    "name": structure.name,
                    "phone": structure.phone,
                    "email": "another@email.com",
                    "address_line_1": structure.address1,
                    "address_line_2": "",
                    "post_code": structure.postal_code,
                    "city": structure.city,
                    "department": structure.department,
                    "website": structure.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure.full_desc,
                    "source_link": structure.get_absolute_url(),
                },
            ],
        )

    def test_no_sync_on_model_save_no_changed_data(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            structure.save()
        assert mock_nexus_api.calls == []

    def test_no_sync_on_model_save_non_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            structure.image_name = "img.png"
            structure.save()
        assert mock_nexus_api.calls == []

    def test_delete_on_model_save(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        with django_capture_on_commit_callbacks(execute=True):
            structure_1 = make_structure(is_obsolete=True)

        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(call, [{"id": str(structure_1.pk)}])

    def test_delete_on_model_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure = make_structure()
        structure_id = structure.pk

        with django_capture_on_commit_callbacks(execute=True):
            structure.delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(call, [{"id": str(structure_id)}])

    def test_sync_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure_1 = make_structure()
        structure_2 = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            Structure.objects.order_by("pk").update(name="Monster Inc")
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {
                    "id": str(structure_1.pk),
                    "kind": structure_1.typology,
                    "siret": structure_1.siret,
                    "name": "Monster Inc",
                    "phone": structure_1.phone,
                    "email": structure_1.email,
                    "address_line_1": structure_1.address1,
                    "address_line_2": "",
                    "post_code": structure_1.postal_code,
                    "city": structure_1.city,
                    "department": structure_1.department,
                    "website": structure_1.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure_1.full_desc,
                    "source_link": structure_1.get_absolute_url(),
                },
                {
                    "id": str(structure_2.pk),
                    "kind": structure_2.typology,
                    "siret": structure_2.siret,
                    "name": "Monster Inc",
                    "phone": structure_2.phone,
                    "email": structure_2.email,
                    "address_line_1": structure_2.address1,
                    "address_line_2": "",
                    "post_code": structure_2.postal_code,
                    "city": structure_2.city,
                    "department": structure_2.department,
                    "website": structure_2.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure_2.full_desc,
                    "source_link": structure_2.get_absolute_url(),
                },
            ],
        )

    def test_delete_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure_1 = make_structure()
        structure_2 = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            Structure.objects.order_by("pk").update(is_obsolete=True)
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {"id": str(structure_1.pk)},
                {"id": str(structure_2.pk)},
            ],
        )

    def test_delete_on_manager_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure_1 = make_structure()
        structure_2 = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            Structure.objects.order_by("pk").delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {"id": str(structure_1.pk)},
                {"id": str(structure_2.pk)},
            ],
        )

    def test_sync_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure_1 = make_structure()
        structure_2 = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            structure_1.name = "Monster Inc"
            structure_2.name = "Monster & Cie"
            Structure.objects.bulk_update([structure_1, structure_2], ["name"])
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {
                    "id": str(structure_1.pk),
                    "kind": structure_1.typology,
                    "siret": structure_1.siret,
                    "name": "Monster Inc",
                    "phone": structure_1.phone,
                    "email": structure_1.email,
                    "address_line_1": structure_1.address1,
                    "address_line_2": "",
                    "post_code": structure_1.postal_code,
                    "city": structure_1.city,
                    "department": structure_1.department,
                    "website": structure_1.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure_1.full_desc,
                    "source_link": structure_1.get_absolute_url(),
                },
                {
                    "id": str(structure_2.pk),
                    "kind": structure_2.typology,
                    "siret": structure_2.siret,
                    "name": "Monster & Cie",
                    "phone": structure_2.phone,
                    "email": structure_2.email,
                    "address_line_1": structure_2.address1,
                    "address_line_2": "",
                    "post_code": structure_2.postal_code,
                    "city": structure_2.city,
                    "department": structure_2.department,
                    "website": structure_2.url,
                    "opening_hours": "",
                    "accessibility": "",
                    "description": structure_2.full_desc,
                    "source_link": structure_2.get_absolute_url(),
                },
            ],
        )

    def test_delete_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        structure_1 = make_structure()
        structure_2 = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            structure_1.is_obsolete = True
            structure_2.is_obsolete = True
            Structure.objects.bulk_update([structure_1, structure_2], ["is_obsolete"])
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/structures"
        assert_call_content(
            call,
            [
                {"id": str(structure_1.pk)},
                {"id": str(structure_2.pk)},
            ],
        )


class TestStructureMemberSync:
    def test_sync_on_model_save_new_instance(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        user = make_syncable_user()
        structure = make_structure()

        with django_capture_on_commit_callbacks(execute=True):
            membership = make_structure_member(user=user, structure=structure)
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {
                    "id": str(membership.pk),
                    "user_id": str(membership.user.pk),
                    "structure_id": str(membership.structure.pk),
                    "role": "COLLABORATOR",
                },
            ],
        )

    def test_sync_on_model_save_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()

        with django_capture_on_commit_callbacks(execute=True):
            membership.is_admin = True
            membership.save()
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {
                    "id": str(membership.pk),
                    "user_id": str(membership.user.pk),
                    "structure_id": str(membership.structure.pk),
                    "role": "ADMINISTRATOR",
                },
            ],
        )

    def test_no_sync_on_model_save_no_change(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()

        with django_capture_on_commit_callbacks(execute=True):
            membership.save()
        assert mock_nexus_api.calls == []

    def test_no_sync_on_model_save_non_tracked_field(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()

        with django_capture_on_commit_callbacks(execute=True):
            membership.created_at = timezone.now()
            membership.save()
        assert mock_nexus_api.calls == []

    def test_delete_on_model_save(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()
        membership.structure.is_obsolete = True
        membership.structure.save()
        other_user = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            membership.user = other_user
            membership.save()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(call, [{"id": str(membership.pk)}])

    def test_sync_on_model_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()

        with django_capture_on_commit_callbacks(execute=True):
            membership_id = membership.pk
            membership.delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(call, [{"id": str(membership_id)}])

    def test_sync_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()
        user_2 = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            StructureMember.objects.update(user=user_2)
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {
                    "id": str(membership.pk),
                    "user_id": str(user_2.pk),
                    "structure_id": str(membership.structure.pk),
                    "role": "COLLABORATOR",
                },
            ],
        )

    def test_delete_on_manager_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership = make_syncable_member()
        inactive_user = make_syncable_user(is_active=False)

        with django_capture_on_commit_callbacks(execute=True):
            StructureMember.objects.order_by("pk").update(user=inactive_user)
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(call, [{"id": str(membership.pk)}])

    def test_delete_on_manager_delete(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership_1 = make_syncable_member()
        membership_2 = make_syncable_member()

        with django_capture_on_commit_callbacks(execute=True):
            StructureMember.objects.order_by("pk").delete()
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {"id": str(membership_1.pk)},
                {"id": str(membership_2.pk)},
            ],
        )

    def test_sync_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership_1 = make_syncable_member()
        membership_2 = make_syncable_member()
        other_user = make_syncable_user()

        with django_capture_on_commit_callbacks(execute=True):
            membership_1.user = other_user
            membership_2.user = other_user
            StructureMember.objects.bulk_update([membership_1, membership_2], ["user"])
        [call] = mock_nexus_api.calls
        assert call.request.method == "POST"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {
                    "id": str(membership_1.pk),
                    "user_id": str(other_user.pk),
                    "structure_id": str(membership_1.structure.pk),
                    "role": "COLLABORATOR",
                },
                {
                    "id": str(membership_2.pk),
                    "user_id": str(other_user.pk),
                    "structure_id": str(membership_2.structure.pk),
                    "role": "COLLABORATOR",
                },
            ],
        )

    def test_delete_on_manager_bulk_update(
        self, db, django_capture_on_commit_callbacks, mock_nexus_api
    ):
        membership_1 = make_syncable_member()
        membership_2 = make_syncable_member()
        obsolete_structure = make_structure(is_obsolete=True)

        with django_capture_on_commit_callbacks(execute=True):
            membership_1.structure = obsolete_structure
            membership_2.structure = obsolete_structure
            StructureMember.objects.bulk_update(
                [membership_1, membership_2], ["structure"]
            )
        [call] = mock_nexus_api.calls
        assert call.request.method == "DELETE"
        assert call.request.url == "http://nexus/api/memberships"
        assert_call_content(
            call,
            [
                {"id": str(membership_1.pk)},
                {"id": str(membership_2.pk)},
            ],
        )
