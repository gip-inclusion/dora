#!/usr/bin/env bash

set -e
set -o pipefail

CURRENT_DIR=$(pwd)
MERGE_COMMIT_MESSAGE="MEP $(date +'%d.%m.%Y') : Merge branch 'main' into release"
GIT_BACK_END_URL=git@github.com:gip-inclusion/dora-back.git
GIT_FRONT_END_URL=git@github.com:gip-inclusion/dora-front.git

TEMP_DIR=$(mktemp -d)
echo "Création d'un répertoire temporaire pour le travail : $TEMP_DIR"
cd "$TEMP_DIR"

echo "Clonage du dépôt dora-back..."
git clone $GIT_BACK_END_URL

cd dora-back

echo "Récupération des branches distantes pour dora-back..."
git fetch --all

echo "Changement de branche vers release..."
git switch release

echo "Merge de la branche main dans release pour dora-back..."
git merge --no-ff main -m "$MERGE_COMMIT_MESSAGE"

echo "Poussée des changements vers le dépôt distant pour dora-back..."
git push

cd ..

echo "Clonage du dépôt dora-front..."
git clone $GIT_FRONT_END_URL

cd dora-front

echo "Récupération des branches distantes pour dora-front..."
git fetch --all

echo "Changement de branche vers release..."
git switch release

echo "Merge de la branche main dans release pour dora-front..."
git merge --no-ff main -m "$MERGE_COMMIT_MESSAGE"

echo "Poussée des changements vers le dépôt distant pour dora-front..."
git push

echo "Nettoyage : retour au répertoire initial et suppression du répertoire temporaire."
cd "$CURRENT_DIR"
rm -rf "$TEMP_DIR"