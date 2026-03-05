#!/bin/bash

echo "Synchronisation des données Nexus"
python /app/manage.py nexus_full_sync

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "La synchronisation metabase pour Nexus ne se fait qu'en production"
  exit 0;
fi

echo "Synchronisation metabase pour Nexus"
python /app/manage.py populate_metabase_nexus
