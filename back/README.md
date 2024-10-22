# dora-back

## Pré-requis

- Python 3
- PostgreSQL avec l'extension [PostGIS](https://postgis.net/).
- [GDAL](https://gdal.org/).

### Docker Compose

PostgreSQL, PostGIS, Minio et Redis peuvent être installés simplement avec Docker Compose.

Copier `docker-compose.yml.template` en `docker-compose.yml`.

Vous pouvez modifier `docker-compose.yml` à votre guise (ports, volumes, etc.).

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

- Créer une base de données PostgresQL `dora`.
- Copier le dossier `envs-example` et renommer le `envs`
- Dans le fichier `envs/dev.env`, compléter la variable `POSTGRES_USER`.
- Dans le fichier `envs/secrets.env`, compléter les variables `POSTGRES_PASSWORD` et `DJANGO_SECRET_KEY`.

```bash
# Installer les dépendances
pip install -r requirements/dev.txt

# Vérifier que tout fonctionne
./manage.py check

# Créer les tables de la base de données
./manage.py migrate
```

## Problèmes avec GeoDjango

GeoDjango a besoin des _packages_ `GEOS` et `GDAL` pour fonctionner.

Si Django n'arrive pas à trouver les librairies nécessaires, vous pourrez ajouter les variables d'environnement suivante
à votre shell

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

## Développement

Veillez à ce que la variable d'environnement `DJANGO_SETTINGS_MODULE` soit initialisée
pour que le fichier de configuration de développement soit bien chargé.

```bash
export DJANGO_SETTINGS_MODULE=config.settings.dev
```

```bash
# Démarrer le serveur
./manage.py runserver
```

## Contribution

```bash
# Installer les hooks de pre-commit:
pre-commit install
```

Le pre-commit du projet nécessite une installation locale sur le poste de dev de Talisman (en remplacement de GGShield).
Voir [la procédure d'installation](https://github.com/thoughtworks/talisman?tab=readme-ov-file#installation).
