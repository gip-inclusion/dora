#!/bin/bash

echo "Suppression des pièces jointes des anciennes orientations acceptées"
python /app/manage.py delete_old_closed_orientation_attachments
