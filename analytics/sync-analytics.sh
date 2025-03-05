#!/bin/bash

# This program can also be used to synchronize the source table locally,
# you only have to provide the correct DATABASE_URL and DORA_DATABASE_URL
# with an enabled proxy to the DORA database.

# Chargement des variables d'environnement à partir du fichier .env s'il existe
if [ -f .env ]; then
    echo "Chargement des variables d'environnement à partir du fichier .env"
    source .env
fi

# Vérification si les variables d'environnement requises sont définies
required_vars=("DORA_DATABASE_URL" "DATABASE_URL")
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

if command -v dbclient-fetcher &> /dev/null; then
    dbclient-fetcher pgsql
fi

# Generate the list of tables to be exported
cat models/_sources.yml | grep '      - name' | cut -d':' -f2 > tables.txt
xargs -I {} echo -n "-t {} " < tables.txt > args.txt

time pg_dump $DORA_DATABASE_URL --jobs=8 --format=directory --compress=1 --clean --if-exists --no-owner --no-privileges --verbose $(cat args.txt) --file=/tmp/out.dump
time psql $DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; CREATE EXTENSION IF NOT EXISTS postgis;"
time pg_restore --dbname=$DATABASE_URL --jobs=8 --format=directory --clean --if-exists --no-owner --no-privileges --verbose /tmp/out.dump

# Run DBT model generation & validation
cleaned_url=${DATABASE_URL#postgresql://}
cleaned_url=${cleaned_url#postgres://}
cleaned_url=${cleaned_url#postgres://}

userpass=$(echo "$cleaned_url" | cut -d@ -f1)
export PGUSER=$(echo "$userpass" | cut -d: -f1)
export PGPASSWORD=$(echo "$userpass" | cut -d: -f2)

hostportdb=$(echo "$cleaned_url" | cut -d@ -f2)
export PGHOST=$(echo "$hostportdb" | cut -d: -f1)
export PGPORT=$(echo "$hostportdb" | cut -d: -f2 | cut -d/ -f1)
export PGDATABASE=$(echo "$hostportdb" | cut -d/ -f2 | cut -d'?' -f1)

dbt debug
dbt deps
dbt seed
dbt build
