#!/bin/bash

## Seulement sur la production 
if [ "$ENVIRONMENT" != "production" ];then
  echo "L'envoi des notifications automatiques ne se fait qu'en production"
  exit 0;
fi

echo "Activation des tâches de notification"
python /app/manage.py process_notification_tasks --wet-run
