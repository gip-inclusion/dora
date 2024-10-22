#!/bin/bash

# A NE PAS UTILISER DIRECTEMENT (sans bonne raison) :
# script lancé par 'update-metabase-db.sh`

export DEST_DB_URL=$METABASE_DB_URL

# Suppression en cascade et "à la main" de tables
# L'instruction ci-dessous pg_dump $DATABASE_URL ... | psql -q $DEST_DB_URL ne
# supprime pas corectement les tables, ce qui créée des doublons de données.
psql $DEST_DB_URL -c "
DO \$\$
DECLARE
    r RECORD;
BEGIN
    FOR r IN
        SELECT tablename
        FROM pg_tables
        WHERE tablename LIKE 'structures_%'
        OR tablename LIKE 'stats_%'
        OR tablename LIKE 'orientations_%'
    LOOP
        EXECUTE 'DROP TABLE ' || r.tablename || ' CASCADE';
    END LOOP;
END \$\$;
"

# Export des tables vers METABASE
pg_dump $DATABASE_URL -O -c --if-exists -t orientations_* -t stats_*  -t structures_* -t services_servicesource -t services_bookmark -t services_servicefee -t services_accesscondition -t services_beneficiaryaccessmode -t services_coachorientationmode -t services_concernedpublic -t services_credential -t services_locationkind -t services_requirement -t services_service_access_conditions -t services_service_beneficiaries_access_modes -t services_service_categories -t services_service_coach_orientation_modes -t services_service_concerned_public -t services_service_credentials -t services_service_kinds -t services_service_location_kinds -t services_service_requirements -t services_service_subcategories -t services_servicecategory -t services_servicekind -t services_servicemodificationhistoryitem -t services_servicestatushistoryitem -t services_servicesubcategory -t services_savedsearch -t services_savedsearch_fees -t services_savedsearch_kinds -t services_savedsearch_subcategories  | psql -q $DEST_DB_URL
