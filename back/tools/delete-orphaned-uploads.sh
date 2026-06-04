#!/bin/bash

echo "Suppression des documents inutiles dans le stockage s3"
python /app/manage.py delete_orphaned_uploads --wet-run
