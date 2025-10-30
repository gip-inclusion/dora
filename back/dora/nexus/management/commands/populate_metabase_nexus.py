"""
Populate metabase database with data for nexus analysis

All the required code is maintained in this command so that we can easily re-use it in
the other projects.
"""

import logging

import psycopg
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from psycopg import sql

from dora.structures.models import StructureMember, Structure
from dora.users.models import User


logger = logging.getLogger(__name__)

SOURCE = "dora"  # Change in each product
USER_TABLE = "users"
MEMBERSHIPS_TABLE = "memberships"
STRUCTURES_TABLE = "structures"


def get_connection():
    return psycopg.connect(
        host=settings.NEXUS_METABASE_DB_HOST,
        port=settings.NEXUS_METABASE_DB_PORT,
        dbname=settings.NEXUS_METABASE_DB_DATABASE,
        user=settings.NEXUS_METABASE_DB_USER,
        password=settings.NEXUS_METABASE_DB_PASSWORD,
        keepalives=1,
        keepalives_idle=30,
        keepalives_interval=5,
        keepalives_count=5,
    )


def create_table():
    if settings.BITOUBI_ENV not in ["dev", "test"]:
        raise ValueError

    # Only used in tests: only les-emplois is supposed to call it for real
    with get_connection() as conn, conn.cursor() as cursor:
        cursor.execute(f"DROP TABLE IF EXISTS {USER_TABLE}")
        cursor.execute(f"DROP TABLE IF EXISTS {MEMBERSHIPS_TABLE}")
        cursor.execute(f"DROP TABLE IF EXISTS {STRUCTURES_TABLE}")
        cursor.execute(
            f"""
            CREATE TABLE {USER_TABLE} (
                source              text NOT NULL,
                id_source           text NOT NULL,
                id_unique           text NOT NULL,
                nom                 text NOT NULL,
                prénom              text NOT NULL,
                email               text NOT NULL,
                téléphone           text NOT NULL,
                dernière_connexion  timestamp with time zone,
                auth                text NOT NULL,
                type                text NOT NULL,
                mise_à_jour         timestamp with time zone
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE {MEMBERSHIPS_TABLE} (
                source                  text NOT NULL,
                user_id_unique          text NOT NULL,
                structure_id_unique     text NOT NULL,
                role                    text NOT NULL,
                mise_à_jour             timestamp with time zone
            )
            """
        )
        cursor.execute(
            f"""
            CREATE TABLE {STRUCTURES_TABLE} (
                source      text NOT NULL,
                id_source   text NOT NULL,
                id_unique   text NOT NULL,
                siret       text,
                nom         text NOT NULL,
                type        text NOT NULL,
                code_insee  text,
                adresse     text,
                code_postal text,
                latitude    double precision,
                longitude   double precision,
                email       text NOT NULL,
                téléphone   text NOT NULL,
                mise_à_jour timestamp with time zone
            )
            """
        )


def populate_table(table_name, table_columns, serializer, querysets):
    with get_connection() as conn, conn.cursor() as cur:
        cur.execute(f"DELETE FROM {table_name} WHERE source = '{SOURCE}'")
        for queryset in querysets:
            with cur.copy(
                sql.SQL(
                    "COPY {table_name} ({fields}) FROM STDIN WITH (FORMAT BINARY)"
                ).format(
                    table_name=sql.Identifier(table_name),
                    fields=sql.SQL(",").join(
                        [sql.Identifier(name) for name in table_columns.keys()],
                    ),
                )
            ) as copy:
                copy.set_types(table_columns.values())
                for row in queryset.iterator():
                    copy.write_row(serializer(row))


def log_retry_attempt(retry_state):
    logger.info("Attempt failed with outcome=%s", retry_state.outcome)


class Command(BaseCommand):
    help = "Populate nexus metabase database."

    def populate_users(self):
        queryset = User.objects.filter(
            is_active=True,
            email__isnull=False,
            # FIXME: more filters ?
        )

        def serializer(user):
            return [
                SOURCE,
                str(user.pk),
                f"{SOURCE}--{user.pk}",
                user.last_name,
                user.first_name,
                user.email,
                str(user.phone),
                user.last_login,
                "ProConnect" if user.sub_pc else "Magic Link",
                "",  # employeur / prescripteur ?
                self.run_at,
            ]

        columns = {
            "source": "text",
            "id_source": "text",
            "id_unique": "text",
            "nom": "text",
            "prénom": "text",
            "email": "text",
            "téléphone": "text",
            "dernière_connexion": "timestamp with time zone",
            "auth": "text",
            "type": "text",
            "mise_à_jour": "timestamp with time zone",
        }

        populate_table(USER_TABLE, columns, serializer, [queryset])

    def populate_memberships(self):
        queryset = StructureMember.objects.filter(user__is_active=True).select_related(
            "structure"
        )

        def serializer(membership):
            return [
                SOURCE,
                f"{SOURCE}--{membership.user_id}",
                membership.structure.data_inclusion_id
                or f"{SOURCE}--{membership.structure_id}",
                "administrateur" if membership.is_admin else "collaborateur",
                self.run_at,
            ]

        columns = {
            "source": "text",
            "user_id_unique": "text",
            "structure_id_unique": "text",
            "role": "text",
            "mise_à_jour": "timestamp with time zone",
        }

        populate_table(MEMBERSHIPS_TABLE, columns, serializer, [queryset])

    def populate_structures(self):
        queryset = Structure.objects.filter(
            # FIXME exclude inactive structures ?
        )

        def serializer(org):
            return [
                SOURCE,
                str(org.pk),
                f"{SOURCE}--{org.pk}",
                org.data_inclusion_id or f"{SOURCE}--{org.id}",
                org.siret,
                org.name,
                org.typology,
                "",
                f"{org.address}, {org.post_code} {org.city}",
                org.post_code,
                org.latitude,
                org.longitude,
                org.email,
                org.phone,
                self.run_at,
            ]

        columns = {
            "source": "text",
            "id_source": "text",
            "id_unique": "text",
            "siret": "text",
            "nom": "text",
            "type": "text",
            "code_insee": "text",
            "adresse": "text",
            "code_postal": "text",
            "latitude": "double precision",
            "longitude": "double precision",
            "email": "text",
            "téléphone": "text",
            "mise_à_jour": "timestamp with time zone",
        }

        populate_table(STRUCTURES_TABLE, columns, serializer, querysets=[queryset])

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset-tables",
            action="store_true",
            default=False,
            help="Reset the table schema",
        )

    def handle(self, *args, reset_tables=False, **kwargs):
        if reset_tables:
            create_table(reset=True)
        else:
            self.run_at = timezone.now()
            self.populate_users()
            self.populate_memberships()
            self.populate_structures()
