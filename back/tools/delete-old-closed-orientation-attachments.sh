#!/bin/bash

echo "Suppression des pièces jointes des anciennes orientations fermées"
python /app/manage.py delete_old_closed_orientation_attachments
