#!/usr/bin/env bash

set -e
set -o pipefail

# Variables globales
CURRENT_DIR=$(pwd)
DORA_REPOSITORY_URL=git@github.com:gip-inclusion/dora.git
DORA_REPOSITORY_NAME=dora

# Couleurs ANSI
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color (reset)

# ===
# 1. PREPARE
# ===

echo ""
echo -e "${YELLOW}🔎 Validations avant lancement de la procédure de livraison${NC}"
echo ""

# ---
# Check param(s)
# ---

echo -e "Vérification des arguments"
if [ -z "$1" ]; then
  echo -e "${RED}⚠️  Vous devez spécifier le type de release (major, minor, patch).${NC}"
  exit 1
fi

RELEASE_TYPE=$1

echo -e "Vérification du type de livraison (parmi "major", "minor" ou "patch")"
if [[ "$RELEASE_TYPE" != "major" && "$RELEASE_TYPE" != "minor" && "$RELEASE_TYPE" != "patch" ]]; then
  echo -e "${RED}⚠️  Type de release invalide : '$RELEASE_TYPE'. Utilisez uniquement 'major', 'minor' ou 'patch'.${NC}"
  exit 1
fi

# ---
# Check environment variables
# ---

check_env_var() {
  local var_name=$1
  if [ -z "${!var_name}" ]; then
    echo -e "${RED}⚠️  La variable d'environnement $var_name doit être définie.${NC}"
    exit 1
  fi
}

echo -e "Vérification des variables d'environnement"
check_env_var "SCALINGO_REGION"
check_env_var "SCALINGO_BACK_APP"
check_env_var "SCALINGO_FRONT_APP"

# ---
# Check Scalingo concerns
# ---

echo -e "Vérification du CLI Scalingo"
if ! command -v scalingo &> /dev/null; then
  echo -e "${RED}⚠️  Le CLI Scalingo n'est pas installé. Veuillez l'installer avant d'exécuter ce script.${NC}"
  exit 1
fi

echo -e "Vérification des accès aux applications Scalingo"
APPS_LIST=$(scalingo apps --region "$SCALINGO_REGION")

check_app_access() {
  local app_name=$1
  if echo "$APPS_LIST" | grep -E "^\|[[:space:]]*$app_name[[:space:]]*\|[[:space:]]*collaborator[[:space:]]*\|" &> /dev/null; then
    echo -e "Accès confirmé pour l'application '$app_name'."
  else
    echo -e "${RED}⚠️  Vous n'avez pas accès en tant que collaborateur à l'application '$app_name' dans la région '$SCALINGO_REGION'. Veuillez vérifier vos permissions.${NC}"
    exit 1
  fi
}

check_app_access "$SCALINGO_BACK_APP"
check_app_access "$SCALINGO_FRONT_APP"

# ---
# Utils
# ---

get_next_version() {
  local version=$1
  local release_type=$2

  # Supprimer le 'v' au début et séparer en parties (major.minor.patch)
  version="${version#v}"
  IFS='.' read -r major minor patch <<< "$version"

  case $release_type in
    major)
      major=$((major + 1))
      minor=0
      patch=0
      ;;
    minor)
      minor=$((minor + 1))
      patch=0
      ;;
    patch)
      patch=$((patch + 1))
      ;;
    *)
      echo -e "${RED}⚠️  Type de release non valide. Utilisez major, minor ou patch.${NC}"
      exit 1
      ;;
  esac

  echo "v$major.$minor.$patch"
}

# ===
# 2. PERFORM
# ===

echo ""
echo -e "${YELLOW}🚀 Lancement de la procédure de livraison${NC}"
echo ""

TEMP_DIR=$(mktemp -d)
echo "✨ Création d'un répertoire temporaire pour le travail : $TEMP_DIR"
cd "$TEMP_DIR"
echo ""

# Déploiement

echo -e "🐑 Clonage du dépôt $DORA_REPOSITORY_NAME..."
echo ""
git clone "$DORA_REPOSITORY_URL"
cd "$DORA_REPOSITORY_NAME"

echo ""
echo -e "🚰 Récupération des tags existants"
echo ""
git fetch --all

# Récupérer le dernier tag pour déterminer la version actuelle
CURRENT_VERSION=$(git describe --tags $(git rev-list --tags --max-count=1))
if [ -z "$CURRENT_VERSION" ]; then
  echo -e "${RED}⚠️ Aucun tag de version trouvé. Assurez-vous qu'un tag existe dans le dépôt.${NC}"
  exit 1
fi

# Vérifier si le tag de la version actuelle existe déjà sur le dernier commit de main
MAIN_COMMIT_HASH=$(git rev-parse main)
TAG_COMMIT_HASH=$(git rev-list -n 1 "$CURRENT_VERSION" 2>/dev/null || echo "")

if [ "$MAIN_COMMIT_HASH" == "$TAG_COMMIT_HASH" ]; then
  echo -e "${YELLOW}🙅 La version '$CURRENT_VERSION' est déjà déployée pour le dernier commit de main. Aucun nouveau déploiement nécessaire.${NC}"
else
  echo -e "💡 Il y a des modifications non déployées dans la branche 'main'. Création d'une nouvelle version..."
  echo ""

  # Incrémenter la version et définir le nouveau tag
  NEW_VERSION=$(get_next_version "$CURRENT_VERSION" "$RELEASE_TYPE")
  echo -e "${CYAN}📌 Création du tag $NEW_VERSION (basée sur le type $RELEASE_TYPE)${NC}"
  echo ""

  git tag "$NEW_VERSION"
  git push origin "$NEW_VERSION"

  echo ""
  echo -e "${CYAN}🚀 Déploiement de l'archive sur Scalingo pour les applications dora-back et dora-front${NC}"
  echo ""
  tag_archive_url="https://github.com/gip-inclusion/dora/archive/refs/tags/$NEW_VERSION.tar.gz"
  
  # TODO : paralléliser les déploiements

  echo -e "Déploiement de l'application back-end"
  echo ""
  scalingo deploy --region "$SCALINGO_REGION" --app "$SCALINGO_BACK_APP" "$tag_archive_url"
  echo ""

  echo -e "Déploiement de l'application front-end"
  echo ""
  scalingo deploy --region "$SCALINGO_REGION" --app "$SCALINGO_FRONT_APP" "$tag_archive_url"
  echo ""
fi

# Revenir au répertoire temporaire
cd ..
echo ""

# Nettoyage
echo -e "🧹 Nettoyage : retour au répertoire initial et suppression du répertoire temporaire."
cd "$CURRENT_DIR"
rm -rf "$TEMP_DIR"
echo ""

# Fin
echo -e "${GREEN}🎉 Fin de la procédure de livraison${NC}"
echo ""
trap - EXIT