# dora-back

## Pré-requis

- Python 3
- PostgreSQL avec l'extension [PostGIS](https://postgis.net/).
- [GDAL](https://gdal.org/).

### Setup des variables d'environnement

Si vous utilisez l'environnement Docker Compose fourni par défaut :
```bash
  ln -s envs-example envs
```
Sinon :
- Copier le dossier `envs-example` et renommer le `envs`
- Modifier les variables nécessaires

### Docker Compose

PostgreSQL, PostGIS, Minio et Redis peuvent être installés simplement avec Docker Compose.

Vous pouvez surcharger le `docker-compose.yml` fournis par défaut en créant un fichier `docker-compose.override.yml` : https://docs.docker.com/compose/how-tos/multiple-compose-files/merge/.

Créer et démarrer les conteneurs :

```bash
docker compose up
```

Importer une sauvegarde de base de données anonymisée :

```bash
docker compose exec -T db psql dora -U POSTGRES_USER < dump-anon.sql
```

Utiliser _psql_ :

```bash
docker compose exec db psql dora -U POSTGRES_USER
```

Accéder à pgAdmin 4 via http://localhost:8888/ en utilisant l'adresse e-mail et le mot de passe configurés par les variables d'environnement `PGADMIN_DEFAULT_EMAIL` et `PGADMIN_DEFAULT_PASSWORD`. Le nom d'hôte de la base de données est `db`.

## Installation


# Installer graphviz
Pour Mac:
```bash
brew install graphviz
```
Pour Linux:
```bash
sudo apt install graphviz
```

Les consignes d'installation sont [ici](https://graphviz.org/download/).'

# Installer libmagic
Pour Mac:
```bash
brew install libmagic
```
Pour Linux:
```bash
sudo apt-get install libmagic1
```

# Installer les dépendances
```bash
pip install -r requirements/dev.txt
```

Vous pouvez aussi utiliser la recette `venv` du Makefile pour créer et/ou mettre à jour votre _virtualenv_,
celle-ci a besoin du petit utilitaire [`uv`](https://docs.astral.sh/uv/getting-started/installation/) installer sur votre système :

```bash
make venv
```

# Vérifier que tout fonctionne
```bash
./manage.py check
```

# Créer les tables de la base de données
```bash
./manage.py migrate
```

Pour que l’application soit utilisable, il faut _a minima_ importer les données géographiques et les labels nationaux :

Pour faire tourner `import_admin_express` localement, il faut installer 7zip

Pour Mac :
```bash
brew install p7zip
```

Pour Linux :
```bash
sudo apt-get install p7zip*
```

```bash
./manage.py import_admin_express
./manage.py loaddata dora/structures/fixtures/01_structure_national_labels.json.gz
# Ou make populate_db
```

Mais pour avoir un jeu de données complet, il est plus simple d’importer la base de _staging_ entière.

# Configurer le téléchargement de documents en local
Vous devez créer un bucket dans Minio pour les téléchargements de documents.

1. Allez sur http://localhost:9001/ et connectez-vous avec les identifiants par défaut :
  - Nom d'utilisateur : minio (configuré dans `envs/dev.env`)
  - Mot de passe : miniosecret (configuré dans `envs/dev.env`)
2. Créez un bucket nommé `dora`.
3. Créez une clé d'accès et copiez la clé d'accès et la clé secrète.
4. Dans `envs/secrets.env`, définissez les variables suivantes :
    - AWS_ACCESS_KEY_ID=<votre_clé_d'accès>
    - AWS_SECRET_ACCESS_KEY=<votre_clé_secrète>


## Problèmes avec GeoDjango

GeoDjango a besoin des _packages_ `GEOS` et `GDAL` pour fonctionner.

Si Django n'arrive pas à trouver les librairies nécessaires, vous pourrez ajouter les variables d'environnement suivante
à votre shell

C'est possible que vous ayez besoin d'installer `gdal`.
Pour Mac:
```bash
brew install gdal
```
Les consignes d'installation sont [ici](https://gdal.org/en/stable/download.html).

```bash
export GDAL_LIBRARY_PATH=
export GEOS_LIBRARY_PATH=
```

Exemple sur Mac M1 avec gdal installé via homebrew :

```bash
export GDAL_LIBRARY_PATH="/opt/homebrew/opt/gdal/lib/libgdal.dylib"
export GEOS_LIBRARY_PATH="/opt/homebrew/opt/geos/lib/libgeos_c.dylib"
```

Pour en savoir plus :

- https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/geolibs/
- https://docs.djangoproject.com/en/4.0/ref/contrib/gis/install/#libsettings

### Erreur on Mac M1

Sur un Mac M1 Silicon, vous pouvez rencontrer l'erreur suivante :

```
ld: library not found for -lssl
clang: error: linker command failed with exit code 1 (use -v to see invocation)
error: command 'clang' failed with exit status 1

× Encountered error while trying to install package.
╰─> psycopg2-binary
```

Vous pouvez corriger ce souci en ajoutant les variables d'environnement suivante à votre shell :

```
export PATH="/opt/homebrew/opt/openssl@3/bin:$PATH"
export LIBRARY_PATH=$LIBRARY_PATH:/opt/homebrew/opt/openssl@3/lib/
```

### Erreur avec Minio
Si vous rencontrez une erreur avec Minio où vous voyez des dizaines de logs comme celui-ci :

```
Adding local Minio host to 'mc' configuration...
```
Suivi par :
```
INFO  ==> MinIO is already stopped...
```

Supprimer le conteneur `s3` :

```bash
docker compose stop s3
docker compose rm -v s3
```

Utilisez une version spécifique de l'image au lieu de `minio/minio:latest` comme par exemple : `minio/minio:RELEASE.2024-01-16T16-07-38Z`
La liste de toutes les versions disponibles est [ici](https://hub.docker.com/r/minio/minio/tags).

Pour recréer les conteneurs :
```bash
docker compose up --build
```

## Développement

Veillez à ce que la variable d'environnement `DJANGO_SETTINGS_MODULE` soit initialisée
pour que le fichier de configuration de développement soit bien chargé.

```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
```

```bash
# Démarrer le serveur
./manage.py runserver # Ou make runserver
```

## Contribution

```bash
# Installer les hooks de pre-commit:
pre-commit install
```

Le pre-commit du projet nécessite une installation locale sur le poste de dev de Talisman (en remplacement de GGShield).
Voir [la procédure d'installation](https://github.com/thoughtworks/talisman?tab=readme-ov-file#installation).

Vous pouvez aussi utiliser les recettes `quality` et `fix` du fichier Makefile :
```bash
make fix
make quality
```

Pour lancer la suite de tests :
```bash
pytest # Ou make test
```
