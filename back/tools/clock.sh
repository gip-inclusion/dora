#!/usr/bin/env bash
#
# Ce script est un ordonnanceur de tâches. Il est exécuté comme
# Custom Clock Process sur Scalingo.
#
# https://doc.scalingo.com/platform/app/task-scheduling/custom-clock-processes
#
# On l'utilise en alternative au Scalingo Scheduler pour exécuter des
# tâches durant plus de 15 minutes.
#
# Il exécute la commande `reset-database.sh` tous les jours à 2h00 UTC.
#

set -e
set -o pipefail

DIRNAME=$(dirname "$0")

while true; do
  current_time=$(date +%H:%M)
  if [ "$current_time" == "02:00" ]; then
    # Exécute reset-database.sh tous les jours à 2h00 UTC
    "${DIRNAME}/reset-database.sh" &
  fi
  sleep 1m
done
