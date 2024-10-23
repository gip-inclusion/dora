#!/bin/bash

set -e
set -o pipefail

# Couleurs ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color (reset)

# Vérification de la présence du endpoint Metabase dans l'environnement 
if [ -z "$METABASE_DB_URL" ];then echo "Pas de serveur Metabase connu ; export abandonné."; exit 0; fi

echo -e "${CYAN}→ Installation de la dernière version de \`psql\`${NC}"
dbclient-fetcher psql
echo " "

echo -e "${CYAN}→ Désactive les messages de niveau \"NOTICE\"${NC}"
psql $METABASE_DB_URL -c "SET client_min_messages TO WARNING;"
echo " "

echo -e "${CYAN}→ Installation et export des requêtes SQL du dossier \`queries\`${NC}"
echo -e "${YELLOW}  tools/utils/install-sql-scripts.sh queries${NC}"
tools/utils/install-sql-scripts.sh queries 
echo " "

echo -e "${CYAN}→ Export des tables de production restantes vers Metabase${NC}"
echo -e "${YELLOW}  tools/utils/export-db-metabase.sh${NC}"
tools/utils/export-db-metabase.sh
echo " "

echo -e "${CYAN}→ Synchronisation du schéma de la base de données dans Metabase${NC}"
echo -e "${YELLOW}  tools/utils/sync-metabase-schemas.sh${NC}"
tools/utils/sync-metabase-schemas.sh
echo " "

echo -e "${CYAN}→ Réactive les messages de niveau \"NOTICE\"${NC}"
psql $METABASE_DB_URL -c "SET client_min_messages TO NOTICE;"
echo " "
