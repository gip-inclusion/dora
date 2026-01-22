import random

from django.db import connection, transaction

from dora.sirene.models import Establishment

"""
Backup lors de l'import SIRENE:
    Outils permettant de créer une table SIRENE temporaire.
    L'objectif et de permettre de créer une base SIRENE à jour,
    sans altérer la version de production, et si possible, à partir d'un conteneur tiers à des fins d'automatisation.
    La démarche :
        - créer une copie vide de la table SIRENE *sans indexes*,
        - importer les données,
        - recréer les indexes,
        - renommer l'ancienne table en `sirene_establiment_bak`,
        - nommer la table nouvellement créée `sirene_establishment`.
    Les ordres sont executés via du SQL "brut", donc toute modification ou optimisation du modèle `sirene`
    entrainera une modification de ces commandes.
    Les indexes sont désactivés en premier lieu pour accélerer *grandemenr* les ordres d'insertion.
    Il sont recréés une fois la table des établissements remplie.
    On pourrait imaginer recréer les DDL via réflexion / introspection, mais c'est de l'over-engineering
    pour une table qui ne bouge ... jamais.
"""


def _suffix():
    return f"{random.getrandbits(16 * 8):8x}"


def create_table(table_name: str):
    create_table_ddl = f"""
    DROP TABLE IF EXISTS public.{table_name};
    CREATE TABLE public.{table_name} (
        siret varchar(14) NOT NULL,
        siren varchar(9) NOT NULL,
        ape varchar(6) NOT NULL,
        city_code varchar(5) NOT NULL,
        postal_code varchar(5) NOT NULL,
        is_siege bool NOT NULL,
        longitude float8 NULL,
        latitude float8 NULL,
        full_search_text text NOT NULL,
        address1 varchar(255) NOT NULL,
        address2 varchar(255) NOT NULL,
        city varchar(255) NOT NULL,
        name varchar(255) NOT NULL,
        parent_name varchar(255) NOT NULL,
        CONSTRAINT {table_name}_{_suffix()}_pkey PRIMARY KEY (siret)
    );
    """
    with connection.cursor() as c:
        c.execute(create_table_ddl)


def create_indexes(table_name: str):
    create_indexes_ddl = f"""
    CREATE INDEX {table_name}_full_text_trgm_{_suffix()}idx ON public.{table_name} USING gin (full_search_text gin_trgm_ops);
    CREATE INDEX {table_name}_code_commune_{_suffix()} ON public.{table_name} USING btree (city_code);
    CREATE INDEX {table_name}_code_commune_{_suffix()}_like ON public.{table_name} USING btree (city_code varchar_pattern_ops);
    CREATE INDEX {table_name}_is_siege_{_suffix()} ON public.{table_name} USING btree (is_siege);
    CREATE INDEX {table_name}_name_{_suffix()} ON public.{table_name} USING btree (name);
    CREATE INDEX {table_name}_name_{_suffix()}_like ON public.{table_name} USING btree (name varchar_pattern_ops);
    CREATE INDEX {table_name}_parent_name_{_suffix()} ON public.{table_name} USING btree (parent_name);
    CREATE INDEX {table_name}_parent_name_{_suffix()}_like ON public.{table_name} USING btree (parent_name varchar_pattern_ops);
    CREATE INDEX {table_name}_siren_{_suffix()} ON public.{table_name} USING btree (siren);
    CREATE INDEX {table_name}_siren_{_suffix()}_like ON public.{table_name} USING btree (siren varchar_pattern_ops);
    CREATE INDEX {table_name}_siret_{_suffix()}_like ON public.{table_name} USING btree (siret varchar_pattern_ops);
    """
    with connection.cursor() as c:
        c.execute(create_indexes_ddl)


def rename_table(orig_table_name: str, dest_table_name: str):
    with connection.cursor() as c:
        # au lieu de :
        # c.execute("ALTER TABLE %s RENAME TO %s;", [orig_table_name, dest_table_name])
        # les placeholders de type `string` sont automatiquement entourés de quotes ('),
        # ce qui vrille les ordres DDL.
        order = f"ALTER TABLE {orig_table_name} RENAME TO {dest_table_name};"
        c.execute(order)


def analyze(table_name: str):
    with connection.cursor() as c:
        c.execute(f"ANALYZE {table_name};")


def clean_tmp_tables(*tmp_tables):
    # attention ...
    with connection.cursor() as c:
        # petite sécurité supplémentaire:
        # les tables temporaires sont obligatoirement préfixées par `_`
        for tmp_table in [tt for tt in tmp_tables if tt.startswith("_")]:
            print(f" > suppression de {tmp_table}")
            c.execute(f"DROP TABLE IF EXISTS {tmp_table}")


def create_insert_statement(table_name: str) -> tuple[str, list[str]]:
    fields = [f.name for f in Establishment._meta.fields]
    stmt = f"INSERT INTO public.{table_name}({','.join(fields)}) VALUES({','.join(['%s'] * len(fields))})"
    return stmt, fields


def add_establishment(stmt: str, e: Establishment, fields: list[str]):
    # non-transactionnel
    values = [getattr(e, f) for f in fields]
    with connection.cursor() as c:
        c.execute(stmt, values)


@transaction.atomic
def bulk_add_establishments(table_name: str, ee: list[Establishment]):
    stmt, fields = create_insert_statement(table_name)
    for e in ee:
        add_establishment(stmt, e, fields)


# --- Legal Units temp table functions ---


def create_legal_units_table(table_name: str):
    create_table_ddl = f"""
    DROP TABLE IF EXISTS public.{table_name};
    CREATE TABLE public.{table_name} (
        siren varchar(9) NOT NULL,
        name varchar(255) NOT NULL,
        CONSTRAINT {table_name}_{_suffix()}_pkey PRIMARY KEY (siren)
    );
    """
    with connection.cursor() as c:
        c.execute(create_table_ddl)


def create_legal_units_index(table_name: str):
    create_index_ddl = f"""
    CREATE INDEX {table_name}_siren_{_suffix()}_idx ON public.{table_name} USING btree (siren);
    """
    with connection.cursor() as c:
        c.execute(create_index_ddl)


@transaction.atomic
def bulk_add_legal_units(table_name: str, rows: list[tuple[str, str]]):
    stmt = f"INSERT INTO public.{table_name}(siren, name) VALUES(%s, %s)"
    with connection.cursor() as c:
        c.executemany(stmt, rows)


def get_legal_units_batch(table_name: str, sirens: list[str]) -> dict[str, str]:
    """Fetch multiple legal unit names in one query, returns {siren: name}"""
    if not sirens:
        return {}
    with connection.cursor() as c:
        placeholders = ",".join(["%s"] * len(sirens))
        c.execute(
            f"SELECT siren, name FROM public.{table_name} WHERE siren IN ({placeholders})",
            sirens,
        )
        return {row[0]: row[1] for row in c.fetchall()}


def drop_table(table_name: str):
    with connection.cursor() as c:
        c.execute(f"DROP TABLE IF EXISTS public.{table_name}")
