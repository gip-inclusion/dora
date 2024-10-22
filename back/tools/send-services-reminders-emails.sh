#!/bin/bash

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "L'envoi des courriels de rappel de mise à jour des services ne se fait qu'en production"
  exit 0;
fi

echo "Envoi des courriels de relance pour les brouillons et services à mettre à jour"
python /app/manage.py send_services_reminders
