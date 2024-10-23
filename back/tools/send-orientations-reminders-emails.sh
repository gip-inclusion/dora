#!/bin/bash

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "L'envoi des courriels de rappel de mise à jour des orientations ne se fait qu'en production"
  exit 0;
fi

echo "Envoi des courriels de relance pour les orientations en attente"
python /app/manage.py send_orientations_reminders
