#!/bin/bash

echo "Suppression des pièces jointes des anciennes orientations acceptées"
python /app/manage.py delete_old_accepted_orientation_attachments
