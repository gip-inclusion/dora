#!/bin/bash

# This program can also be used to synchronize the source table locally,
# you only have to provide the correct DATABASE_URL and DORA_DATABASE_URL
# with an enabled proxy to the DORA database.

load_env_file_if_exists() {
    echo "Load env file if it exists..."

    if [ -f .env ]; then
        echo "Fichier .env trouvé"
        source .env
    fi

    echo "Done."
    echo ""
}

check_required_vars() {
    echo "Check required vars..."

    required_vars=("DORA_DATABASE_URL" "DATABASE_URL" "S3_BUCKET_VARIANT" "S3_ACCESS_KEY" "S3_SECRET_KEY")
    missing_vars=()

    for var in "${required_vars[@]}"; do
        if [ -z "${!var}" ]; then
            missing_vars+=("$var")
        fi
    done

    if [ ${#missing_vars[@]} -ne 0 ]; then
        echo "Erreur : variables d'environnement requises manquantes :"
        for var in "${missing_vars[@]}"; do
            echo "- $var"
        done
        exit 1
    fi

    echo "Done."
    echo ""
}

configure_pg_env() {
    echo "Configure PG environment variables..."

    cleaned_url=${DATABASE_URL#postgresql://}
    cleaned_url=${cleaned_url#postgres://}

    userpass=$(echo "$cleaned_url" | cut -d@ -f1)
    export PGUSER=$(echo "$userpass" | cut -d: -f1)
    export PGPASSWORD=$(echo "$userpass" | cut -d: -f2)

    hostportdb=$(echo "$cleaned_url" | cut -d@ -f2)
    export PGHOST=$(echo "$hostportdb" | cut -d: -f1)
    export PGPORT=$(echo "$hostportdb" | cut -d: -f2 | cut -d/ -f1)
    export PGDATABASE=$(echo "$hostportdb" | cut -d/ -f2 | cut -d'?' -f1)

    echo "Done."
    echo ""
}

fetch_and_export_dora_data() {
    echo "Fetch and export DORA data..."

    # Specific to Scalingo, cf. https://doc.scalingo.com/platform/databases/access#manually-install-the-databases-cli-in-one-off
    # The program dbclient-fetcher on Scalingo downloads various CLI tools, such as psql, pg_dump, pg_restore, pg_ctl, etc.
    # If this script is run outside of Scalingo, you must have these tools successfully installed
    if command -v dbclient-fetcher &>/dev/null; then
        dbclient-fetcher pgsql
    fi

    # Generate the list of tables to be exported
    cat models/_sources.yml | grep '      - name' | cut -d':' -f2 >tables.txt
    xargs -I {} echo -n "-t {} " <tables.txt >args.txt

    time pg_dump $DORA_DATABASE_URL --jobs=8 --format=directory --compress=1 --clean --if-exists --no-owner --no-privileges --verbose $(cat args.txt) --file=/tmp/out.dump
    time psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION IF NOT EXISTS postgis;"
    time pg_restore --dbname=$DATABASE_URL --jobs=8 --format=directory --clean --if-exists --no-owner --no-privileges --verbose /tmp/out.dump

    echo "Done."
    echo ""
}

fetch_and_export_di_data() {
    echo "Fetch and export data·inclusion data..."

    # Installation of tool `duckdb` on Scalingo/Linux
    if command -v duckdb &>/dev/null; then
        echo "duckdb is already installed, skipping download."
    else
        if [[ "$OSTYPE" == linux* ]]; then
            echo "duckdb not found. Installing duckdb..."
            curl -L -o /tmp/duckdb_cli.zip https://github.com/duckdb/duckdb/releases/latest/download/duckdb_cli-linux-amd64.zip
            unzip -o /tmp/duckdb_cli.zip -d /tmp/duckdb
            export PATH="/tmp/duckdb:${PATH}"
            echo "duckdb installed."
        else
            echo "duckdb is not yet installed. "
            exit 1
        fi
    fi

    CURRENT_DATE=$(date +%F)
    MART_URI="${S3_BUCKET_VARIANT}/data/marts/${CURRENT_DATE}/scheduled__${CURRENT_DATE%%/}T00:00:00+00:00"

    # Generate DuckDB SQL file
    DUCKSQL=$(mktemp)

    cat > "$DUCKSQL" <<EOF
INSTALL httpfs;
LOAD httpfs;

CREATE SECRET (
    TYPE s3,
    KEY_ID '$S3_ACCESS_KEY',
    SECRET '$S3_SECRET_KEY',
    ENDPOINT 's3.fr-par.scw.cloud',
    REGION 'fr-par',
    URL_STYLE 'path'
);

INSTALL postgres;
LOAD postgres;

ATTACH 'dbname=$PGDATABASE host=$PGHOST user=$PGUSER password=$PGPASSWORD port=$PGPORT' AS analytics_pg (TYPE postgres);

-- di_structures
DROP TABLE IF EXISTS di_structures;
CREATE TABLE di_structures AS SELECT * FROM read_parquet('s3://$MART_URI/structures.parquet');
DROP TABLE IF EXISTS analytics_pg.public.di_structures;
CREATE TABLE analytics_pg.public.di_structures AS SELECT * FROM di_structures;

-- di_services
DROP TABLE IF EXISTS di_services;
CREATE TABLE di_services AS SELECT * FROM read_parquet('s3://$MART_URI/services.parquet');
DROP TABLE IF EXISTS analytics_pg.public.di_services;
CREATE TABLE analytics_pg.public.di_services AS SELECT * FROM di_services;
EOF

    # Execute SQL export/import orders
    time duckdb < "$DUCKSQL"

    echo "Done."
    echo ""
}

run_dbt_model_generation_and_validation() {
    echo "Run DBT model generation and validation..."

    dbt debug
    dbt deps
    dbt seed
    dbt build

    echo "Done."
    echo ""
}

# Prepare
load_env_file_if_exists
check_required_vars
configure_pg_env

# Perform
fetch_and_export_dora_data
fetch_and_export_di_data
run_dbt_model_generation_and_validation
