#!/usr/bin/env bash

set -e
set -o pipefail

CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color (reset)

REGION=osc-fr1
BACK_REVIEW_APP_TEMPLATE=dora-back-review
FRONT_REVIEW_APP_TEMPLATE=dora-front-review


create_review_app() {
  local review_app_template=$1
  local pr_number=$2

  echo -e "${CYAN}Création de la review app ${review_app_template} pour la PR #${pr_number}…${NC}"
  echo ""
  scalingo --region "${REGION}" --app "${review_app_template}" integration-link-manual-review-app "${pr_number}"
  echo ""
}

main() {
    local pr_number=$1

    echo ""
    create_review_app "${BACK_REVIEW_APP_TEMPLATE}" "${pr_number}"
    create_review_app "${FRONT_REVIEW_APP_TEMPLATE}" "${pr_number}"
}


if [ -z "$1" ]; then
  echo -e "${RED}⚠️  Vous devez spécifier le numéro de la PR.${NC}"
  exit 1
fi

main "$1"
