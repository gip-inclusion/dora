from django.core.management import call_command
from django.utils import timezone
from freezegun import freeze_time

from dora.core.test_utils import make_structure, make_user
from dora.nexus.management.commands.populate_metabase_nexus import (
    create_table,
    get_connection,
)


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
