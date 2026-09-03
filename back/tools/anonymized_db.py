#!/usr/bin/env python3

import argparse
import os
import re
import subprocess
import time
from contextlib import contextmanager
from pathlib import Path
from urllib.parse import urlparse

import environ

ROOT = Path(__file__).resolve().parent.parent
CONFIG = Path(__file__).resolve().parent / "datanymizer-config.yml"
DEFAULT_DUMP = ROOT.parent / "dora-staging.sql"
STAGING_APP = "dora-back-staging"
STAGING_REGION = "osc-fr1"
TUNNEL_PORT = 10001
STAGING_CMD = ["scalingo", "--region", STAGING_REGION, "--app", STAGING_APP]

DROP_STAGING_TABLES = """
DO $$
DECLARE r RECORD;
BEGIN
  FOR r IN (
    SELECT tablename FROM pg_tables
    WHERE schemaname = 'public' AND tablename <> 'spatial_ref_sys'
  ) LOOP
    EXECUTE format('DROP TABLE IF EXISTS %I.%I CASCADE', 'public', r.tablename);
  END LOOP;
END $$;
"""


def psql(pg_url, *args, query=None, input=None, text=None, env=None):
    if query is not None:
        return subprocess.run(
            ["psql", pg_url, "-Atc", query],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
    return subprocess.run(
        ["psql", pg_url, "-v", "ON_ERROR_STOP=1", *args],
        input=input,
        text=text,
        env=env,
        check=True,
    )


def pg_dump(pg_url, *args, capture_output=False):
    return subprocess.run(
        ["pg_dump", pg_url, "--no-owner", *args],
        capture_output=capture_output,
        check=True,
    )


def staging_cmd(*args, capture_output=False):
    return subprocess.run(
        [*STAGING_CMD, *args],
        capture_output=capture_output,
        text=capture_output,
        check=True,
    )


@contextmanager
def scalingo_db_tunnel():
    tunnel_process = subprocess.Popen(
        [*STAGING_CMD, "db-tunnel", "-p", str(TUNNEL_PORT), "DATABASE_URL"],
    )
    try:
        yield tunnel_process
    finally:
        tunnel_process.terminate()
        tunnel_process.wait()


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("dump").add_argument("output", nargs="?", default=DEFAULT_DUMP)
    sub.add_parser("restore-staging").add_argument(
        "dump", nargs="?", default=DEFAULT_DUMP
    )
    args = parser.parse_args()

    os.chdir(ROOT)
    environ.Env.read_env(ROOT / "envs" / "dev.env")
    environ.Env.read_env(ROOT / "envs" / "secrets.env")

    local_pg_url = (
        f"postgresql://{os.environ['POSTGRES_USER']}:"
        f"{os.environ['POSTGRES_PASSWORD']}@"
        f"{os.environ['POSTGRES_HOST']}:{os.environ['POSTGRES_PORT']}/"
        f"{os.environ['POSTGRES_DB']}"
    )

    if args.command == "dump":
        subprocess.run(
            [
                "pg_datanymizer",
                "-c",
                str(CONFIG),
                "-f",
                str(args.output),
                local_pg_url,
                "--",
                "--no-owner",
                "--no-privileges",
            ],
            check=True,
        )
        print(args.output)
        return

    scalingo_pg_url = staging_cmd(
        "env-get", "DATABASE_URL", capture_output=True
    ).stdout.strip()
    staging_tunnel_pg_url = re.sub(
        r"@[^:/]*:[0-9]*", f"@127.0.0.1:{TUNNEL_PORT}", scalingo_pg_url, count=1
    )
    restore_env = {**os.environ, "PGOPTIONS": "-c statement_timeout=0"}

    with scalingo_db_tunnel() as tunnel_process:
        expected_db = urlparse(scalingo_pg_url).path.lstrip("/")
        for _ in range(30):
            if tunnel_process.poll() is not None:
                raise SystemExit("db-tunnel exited (port already in use?)")
            try:
                actual = psql(
                    staging_tunnel_pg_url, query="SELECT current_database()"
                ).strip()
            except subprocess.CalledProcessError:
                time.sleep(1)
                continue
            if actual != expected_db:
                raise SystemExit(
                    f"tunnel points at {actual!r}, expected {expected_db!r}"
                )
            break
        else:
            raise SystemExit("tunnel not ready")

        psql(staging_tunnel_pg_url, input=DROP_STAGING_TABLES, text=True)
        psql(staging_tunnel_pg_url, "-f", str(args.dump), env=restore_env)
        service_count = psql(
            staging_tunnel_pg_url, query="SELECT count(*) FROM services_service"
        ).strip()
        print(f"restored {service_count} services")
        psql(staging_tunnel_pg_url, "-c", "TRUNCATE django_migrations")
        migrations_dump = pg_dump(
            local_pg_url,
            "--data-only",
            "-t",
            "public.django_migrations",
            capture_output=True,
        )
        psql(staging_tunnel_pg_url, input=migrations_dump.stdout)
        local_table_names = psql(
            local_pg_url,
            query="SELECT tablename FROM pg_tables WHERE schemaname='public'",
        ).splitlines()
        staging_table_names = psql(
            staging_tunnel_pg_url,
            query="SELECT tablename FROM pg_tables WHERE schemaname='public'",
        ).splitlines()
        missing_table_names = sorted(
            table_name
            for table_name in local_table_names
            if table_name not in staging_table_names
        )
        if missing_table_names:
            pg_dump_args = ["--schema-only"]
            for table_name in missing_table_names:
                pg_dump_args.extend(["-t", f"public.{table_name}"])
            schema_dump = pg_dump(local_pg_url, *pg_dump_args, capture_output=True)
            psql(staging_tunnel_pg_url, input=schema_dump.stdout)


if __name__ == "__main__":
    main()
