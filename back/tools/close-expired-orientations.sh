#!/bin/bash

## Only run on the production app
if [ "$ENVIRONMENT" != "production" ];then
  echo "L'envoi des courriels pour annoncer les orientations expirées ne se fait qu'en production"
  exit 0;
fi

echo "Clôture automatique des orientations"
python /app/manage.py close_expired_orientations
