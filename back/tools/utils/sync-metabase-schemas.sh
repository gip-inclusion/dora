#!/bin/bash

# Synchronisation des schémas et champs Metabase :
#
# nécessite la présence des variables d'environnement suivantes:
# - METABASE_API_URL          : endpoint de l'API (normallement URL de base + '/api' )
# - METABASE_SERVICE_EMAIL    : e-mail du compte de service pour la création de la session
# - METABASE_SERVICE_PASSWORD : mot de passe du compte de service
# - METABASE_DB_ID            : identifiant interne de la BD (entier, si une seule base : 2)
#                               voir dans l'espace administrateur, rubrique : 'Bases de données'
#                               l'ID est affiché dans l'URL

if [ -z ${METABASE_API_URL} ]; then
	echo " > l'URL de l'API Metabase n'est pas défini"
	exit 1
fi

if [ -z ${METABASE_SERVICE_EMAIL} ]; then
	echo " > l'adresse e-mail du compte de service Metabase n'est pas définie"
	exit 1
fi

if [ -z ${METABASE_SERVICE_PASSWORD} ]; then
	echo " > le mot de passe du compte de service Metabase n'est pas défini"
	exit 1
fi

echo " > connexion à : $METABASE_API_URL"

# récupération de l'ID de session
METABASE_SESSION_ID=$(curl -X POST -H "Content-Type: application/json" -d '{"username":"'"$METABASE_SERVICE_EMAIL"'","password":"'"$METABASE_SERVICE_PASSWORD"'"}' $METABASE_API_URL/session | jq -r ."id")

# Schémas :
curl -X POST -H "X-Metabase-Session: $METABASE_SESSION_ID" $METABASE_API_URL/database/$METABASE_DB_ID/sync_schema
#
# Indexation des champs :
curl -X POST -H "X-Metabase-Session: $METABASE_SESSION_ID" $METABASE_API_URL/database/$METABASE_DB_ID/rescan_values

# par défault le token reste valable 2 semaines, mais autant clôturer la session et le recréer à chaque utilisation
curl -X DELETE -H "X-Metabase-Session: $METABASE_SESSION_ID"  $METABASE_API_URL/session
unset METABASE_SESSION_ID
