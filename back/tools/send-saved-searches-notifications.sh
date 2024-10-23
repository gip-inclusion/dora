#!/bin/bash

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "L'envoi des courriels de notification pour les recherches sauvegardées ne se fait qu'en production"
  exit 0;
fi

echo "Envoi des courriels des alertes sur les recherches sauvegardées"
python /app/manage.py send_saved_searches_notifications
