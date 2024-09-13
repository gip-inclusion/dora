#!/usr/bin/env bash

set -e
set -o pipefail

# Variables globales
CURRENT_DIR=$(pwd)
MERGE_COMMIT_MESSAGE="MEP $(date +'%d.%m.%Y') : Merge branch 'main' into release"
GIT_BACK_END_URL=git@github.com:gip-inclusion/dora-back.git
GIT_FRONT_END_URL=git@github.com:gip-inclusion/dora-front.git

# Fonction pour gérer le processus de déploiement
deploy_repo() {
  local repo_url=$1
  local repo_name=$2
  
  echo "Clonage du dépôt $repo_name..."
  git clone "$repo_url"

  cd "$repo_name"

  echo "Récupération des branches distantes pour $repo_name..."
  git fetch --all

  echo "Changement de branche vers release..."
  git switch release

  # Vérifier s'il y a des commits d'écart entre 'main' et 'release'
  COMMITS_DIFF=$(git rev-list --count release..main)

  if [ "$COMMITS_DIFF" -gt 0 ]; then
    echo "Il y a $COMMITS_DIFF commit(s) d'écart entre 'main' et 'release' pour $repo_name. Lancement du merge..."
    
    echo "Merge de la branche main dans release pour $repo_name..."
    if ! git merge --no-ff main -m "$MERGE_COMMIT_MESSAGE"; then
      echo "Conflit lors du merge de la branche main dans release pour $repo_name. Veuillez résoudre manuellement."
      exit 1
    fi

    echo "Poussée des changements vers le dépôt distant pour $repo_name..."
    git push
  else
    echo "Pas de commits à merger entre 'main' et 'release' pour $repo_name. Aucun merge effectué."
  fi

  # Revenir au répertoire temporaire
  cd ..
}

# Création d'un répertoire temporaire
TEMP_DIR=$(mktemp -d)
echo "Création d'un répertoire temporaire pour le travail : $TEMP_DIR"
cd "$TEMP_DIR"

# Déploiement des dépôts
deploy_repo "$GIT_BACK_END_URL" "dora-back"
deploy_repo "$GIT_FRONT_END_URL" "dora-front"

# Nettoyage
echo "Nettoyage : retour au répertoire initial et suppression du répertoire temporaire."
cd "$CURRENT_DIR"
rm -rf "$TEMP_DIR"