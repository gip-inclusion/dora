import json
import uuid

from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time
from itoutils.django.testing import assertSnapshotQueries

from dora.core.test_utils import make_structure, make_user
from dora.nexus.management.commands.populate_metabase_nexus import (
    create_table,
    get_connection,
)
from dora.nexus.tests.test_sync import assert_call_content, make_syncable_user


@freeze_time()
def test_populate_metabase_nexus(db):
    to_ignore_user = make_user()
    structure = make_structure(
        putative_member=to_ignore_user,
        address1="3 rue de Clery",
        address2="3e escalier",
        postal_code="75002",
        city="Paris",
    )
    user = make_user(structure=structure, is_admin=True)

    create_table()
    call_command("populate_metabase_nexus")

    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute("SELECT * FROM users ORDER BY email")
        rows = cursor.fetchall()
        assert rows == [
            (
                "dora",
                str(user.pk),
                f"dora--{user.pk}",
                user.last_name,
                user.first_name,
                user.email,
                "",
                user.last_login,
                "ProConnect" if user.sub_pc else "Magic Link",
                user.get_main_activity_display(),
                timezone.now(),
            ),
        ]

        cursor.execute("SELECT * FROM memberships ORDER BY structure_id_unique")
        rows = cursor.fetchall()
        assert rows == [
            (
                "dora",
                f"dora--{user.pk}",
                f"dora--{structure.pk}",
                "administrateur",
                timezone.now(),
            ),
        ]

        cursor.execute("SELECT * FROM structures ORDER BY id_unique")
        rows = cursor.fetchall()
        assert rows == [
            (
                "dora",
                str(structure.pk),
                f"dora--{structure.pk}",
                structure.siret,
                structure.name,
                structure.typology,
                "",
                "3 rue de Clery 3e escalier, 75002 Paris",
                structure.postal_code,
                structure.latitude,
                structure.longitude,
                structure.email,
                structure.phone,
                timezone.now(),
            ),
        ]


@freeze_time()
def test_full_sync(db, mock_nexus_api, snapshot):
    to_ignore_user = make_user(is_staff=True)
    structure_1 = make_structure(putative_member=to_ignore_user)
    structure_2 = make_structure()
    user_1 = make_syncable_user(structure=structure_1, is_admin=True)
    user_2 = make_syncable_user(
        structure=structure_2, is_admin=False, sub_pc=uuid.uuid4()
    )
    membership_1 = structure_1.membership.get()
    membership_2 = structure_2.membership.get()

    mock_nexus_api.reset()

    with assertSnapshotQueries(snapshot):
        call_command("nexus_full_sync")

    [
        call_init,
        call_sync_structures,
        call_sync_users,
        call_sync_memberships,
        call_completed,
    ] = mock_nexus_api.calls

    assert call_init.request.method == "POST"
    assert call_init.request.url == "http://nexus/api/sync-start"
    started_at = call_init.response.json()["started_at"]

    assert call_sync_structures.request.method == "POST"
    assert call_sync_structures.request.url == "http://nexus/api/structures"
    assert_call_content(
        call_sync_structures,
        [
            {
                "id": str(structure_1.pk),
                "kind": structure_1.typology,
                "siret": structure_1.siret,
                "name": structure_1.name,
                "phone": structure_1.phone,
                "email": structure_1.email,
                "address_line_1": structure_1.address1,
                "address_line_2": structure_1.address2,
                "post_code": structure_1.postal_code,
                "city": structure_1.city,
                "department": structure_1.department,
                "accessibility": "",
                "description": structure_1.full_desc,
                "opening_hours": "",
                "source_link": structure_1.get_absolute_url(),
                "website": structure_1.url,
            },
            {
                "id": str(structure_2.pk),
                "kind": structure_2.typology,
                "siret": structure_2.siret,
                "name": structure_2.name,
                "phone": structure_2.phone,
                "email": structure_2.email,
                "address_line_1": structure_2.address1,
                "address_line_2": structure_2.address2,
                "post_code": structure_2.postal_code,
                "city": structure_2.city,
                "department": structure_2.department,
                "accessibility": "",
                "description": structure_2.full_desc,
                "opening_hours": "",
                "source_link": structure_2.get_absolute_url(),
                "website": structure_2.url,
            },
        ],
    )

    assert call_sync_users.request.method == "POST"
    assert call_sync_users.request.url == "http://nexus/api/users"
    assert_call_content(
        call_sync_users,
        [
            {
                "id": str(user_1.pk),
                "kind": user_1.main_activity,
                "first_name": user_1.first_name,
                "last_name": user_1.last_name,
                "email": user_1.email,
                "phone": "",
                "last_login": None,
                "auth": "MAGIC_LINK",
            },
            {
                "id": str(user_2.pk),
                "kind": user_2.main_activity,
                "first_name": user_2.first_name,
                "last_name": user_2.last_name,
                "email": user_2.email,
                "phone": "",
                "last_login": None,
                "auth": "PRO_CONNECT",
            },
        ],
    )

    assert call_sync_memberships.request.method == "POST"
    assert call_sync_memberships.request.url == "http://nexus/api/memberships"
    assert_call_content(
        call_sync_memberships,
        [
            {
                "id": str(membership_1.pk),
                "user_id": str(user_1.pk),
                "structure_id": str(structure_1.pk),
                "role": "ADMINISTRATOR",
            },
            {
                "id": str(membership_2.pk),
                "user_id": str(user_2.pk),
                "structure_id": str(structure_2.pk),
                "role": "COLLABORATOR",
            },
        ],
    )

    assert call_completed.request.method == "POST"
    assert call_completed.request.url == "http://nexus/api/sync-completed"
    assert json.loads(call_completed.request.content.decode()) == {
        "started_at": started_at
    }
