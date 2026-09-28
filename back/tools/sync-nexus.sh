#!/bin/bash

echo "Synchronisation des données Nexus"
python /app/manage.py nexus_full_sync
