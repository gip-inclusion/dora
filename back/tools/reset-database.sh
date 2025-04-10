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

echo -e "${CYAN}🔍 Vérification de l’environnement…${NC}"
if [ "${ENVIRONMENT}" != "review" ];then
  echo -e "${RED}❌ La réinitialisation de la base de données ne peut se faire que sur une review app.${NC}"
  exit 0;
fi
echo ""

echo -e "${CYAN}🔧 Vérification des variables d’environnement…${NC}"
undefined_vars=()
for var in "${REQUIRED_ENV_VARS[@]}"; do
  if [ -z "${!var}" ]; then
    undefined_vars+=("$var")
  fi
done

if [ ${#undefined_vars[@]} -ne 0 ]; then
  for var in "${undefined_vars[@]}"; do
    echo -e "${RED}❌ La variable d’environnement $var n’est pas définie.${NC}"
  done
  exit 1
fi
echo ""

if command -v dbclient-fetcher &>/dev/null; then
  echo -e "${CYAN}🐘 Installation des outils PostgreSQL…${NC}"
  dbclient-fetcher pgsql
  echo ""
elif ! command -v pg_restore &> /dev/null; then
  echo -e "${RED}❌ pg_restore n’est pas installé. Veuillez l’installer avant d’exécuter ce script.${NC}"
  exit 1
fi

if command -v install-scalingo-cli &>/dev/null; then
  echo -e "${CYAN}⬇️ Installation de Scalingo CLI…${NC}"
  install-scalingo-cli
  echo ""
elif ! command -v scalingo &> /dev/null; then
  echo -e "${RED}❌ Scalingo CLI n’est pas installé. Veuillez l’installer avant d’exécuter ce script.${NC}"
  exit 1
fi

echo -e "${CYAN}🔐 Vérification de la connexion à Scalingo…${NC}"
echo ""
if ! scalingo whoami; then
  echo -e "${CYAN}🔑 Connexion à Scalingo…${NC}"
  scalingo login --api-token "${SCALINGO_API_TOKEN}"
  echo ""
fi

echo -e "${CYAN}📂 Création d’un répertoire temporaire…${NC}"
temp_dir=$(mktemp -d)
echo -e "${YELLOW}→ Utilisation du répertoire temporaire : $temp_dir${NC}"
cd "$temp_dir"
echo ""

echo -e "${CYAN}📥 Récupération de la dernière sauvegarde de staging…${NC}"
scalingo --region "${DORA_BACK_STAGING_REGION}" --app "${DORA_BACK_STAGING_APP}" --addon "${DORA_BACK_STAGING_ADDON}" backups-download
archive_filename=$(ls *.tar.gz)
echo -e "${YELLOW}→ Fichier : $archive_filename${NC}"
echo ""

echo -e "${CYAN}📦 Décompression de l’archive…${NC}"
tar -xzvf "$archive_filename"
decompressed_filename="${archive_filename%.tar.gz}.pgsql"
echo -e "${YELLOW}→ Fichier : $decompressed_filename${NC}"
echo ""

echo -e "${CYAN}🔄 Restauration des données…${NC}"
pg_restore --clean --if-exists --no-owner --no-privileges --no-comments --dbname "$DATABASE_URL" "$decompressed_filename"
echo ""

echo -e "${CYAN}🧹 Suppression du répertoire temporaire…${NC}"
cd -
rm -rf "$temp_dir"
echo ""

echo -e "${GREEN}✨ Restauration des données terminée !${NC}"
