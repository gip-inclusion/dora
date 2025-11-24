#!/bin/bash

echo "Import des données de découpage administratif"
python /app/manage.py import_decoupage_administratif
