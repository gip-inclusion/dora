#!/bin/bash

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "La synchronisation des utilisateurs pour Nexus ne se fait qu'en production"
  exit 0;
fi

echo "Synchronisation des utilisateurs pour Nexus"
python /app/manage.py populate_metabase_nexus
