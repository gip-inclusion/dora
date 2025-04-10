#!/usr/bin/env bash

set -e
set -o pipefail

# Couleurs ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color (reset)

REQUIRED_ENV_VARS=("ENVIRONMENT" "DORA_BACK_STAGING_REGION" "DORA_BACK_STAGING_APP" "DORA_BACK_STAGING_ADDON" "DATABASE_URL" "SCALINGO_API_TOKEN")

echo -e "${CYAN}🔍 Vérification de l'environnement…${NC}"
if [ "${ENVIRONMENT}" != "review" ];then
  echo -e "${RED}La réinitialisation de la base de données ne peut se faire que sur une review app.${NC}"
  exit 0;
fi
echo ""

echo -e "${CYAN}🛠️  Vérification des variables d'environnement…${NC}"
for var in "${REQUIRED_ENV_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    echo -e "${RED}La variable d'environnement $var n'est pas définie.${NC}"
    exit 1
  fi
done
echo ""

if command -v dbclient-fetcher &>/dev/null; then
  echo -e "${CYAN}🐘  Installation des outils PostgreSQL…${NC}"
  dbclient-fetcher pgsql
  echo ""
elif ! command -v pg_restore &> /dev/null; then
  echo -e "${RED}⚠️  pg_restore n'est pas installé. Veuillez l'installer avant d'exécuter ce script.${NC}"
  exit 1
fi

if command -v install-scalingo-cli &>/dev/null; then
  echo -e "${CYAN}⬇️  Installation de Scalingo CLI…${NC}"
  install-scalingo-cli
  echo ""
elif ! command -v scalingo &> /dev/null; then
  echo -e "${RED}⚠️  Scalingo CLI n'est pas installé. Veuillez l'installer avant d'exécuter ce script.${NC}"
  exit 1
fi

echo -e "${CYAN}🔗  Connexion à Scalingo…${NC}"
scalingo login --api-token "${SCALINGO_API_TOKEN}"
echo ""

echo -e "${CYAN}🗑️  Suppression de tous les fichiers .tar.gz existants…${NC}"
nb_files_to_delete=$(ls *.tar.gz 2>/dev/null | wc -l || echo 0)
rm -f *.tar.gz
echo -e "${YELLOW}→ $nb_files_to_delete fichier(s) supprimé(s)${NC}"
echo ""

echo -e "${CYAN}📥  Récupération de la dernière sauvegarde de staging…${NC}"
scalingo --region "${DORA_BACK_STAGING_REGION}" --app "${DORA_BACK_STAGING_APP}" --addon "${DORA_BACK_STAGING_ADDON}" backups-download
archive_filename=$(ls *.tar.gz)
echo -e "${YELLOW}→ Fichier : $archive_filename${NC}"
echo ""

echo -e "${CYAN}📂  Décompression de l'archive…${NC}"
tar -xzvf "$archive_filename"
decompressed_filename="${archive_filename%.tar.gz}.pgsql"
echo -e "${YELLOW}→ Fichier : $decompressed_filename${NC}"
echo ""

echo -e "${CYAN}🔄  Restauration des données…${NC}"
pg_restore --clean --if-exists --no-owner --no-privileges --no-comments --dbname "$DATABASE_URL" "$decompressed_filename"
echo ""

echo -e "${GREEN}✅  Restauration des données terminée !${NC}"
echo ""
