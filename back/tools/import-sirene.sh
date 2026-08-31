#!/bin/bash

set -e
set -o pipefail

## Seulement sur la production
if [ "$ENVIRONMENT" != "production" ]; then
  echo "L'import de la base SIRENE ne se fait qu'en production"
  exit 0
fi

echo "Import des unités légales (phase 1)"
python /app/manage.py import_sirene --import-units

echo "Import des établissements (phase 2)"
python /app/manage.py import_sirene --import-estab

echo "Activation de la nouvelle table SIRENE"
python /app/manage.py import_sirene --activate

echo "Mise à jour des statistiques de la table SIRENE"
python /app/manage.py import_sirene --analyze
