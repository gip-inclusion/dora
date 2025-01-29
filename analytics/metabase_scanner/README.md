# metabase_scanner

Un simple analyseur de base de métadonnées Metabase pour repérer:
- les sources les plus utilisées
- les mauvaises pratiques à éviter
- les JOINs les plus fréquents
- les questions référençant des questions
- les requêtes natives trop complexes

A l'avenir nous pourrions aussi évaluer les index nécessaires, etc.

## Utilisation

Installer l'application
```bash
$ python3 -m venv .venv
$ . .venv/bin/activate
$ pip install -e .
```

Ouvrir un tunnel SSH vers votre base de données de métadonnées Metabase si nécessaire.

```bash
$ ssh -L local_port: remote_address: remote_port username@server.com
$ scalingo -a app-metabase db-tunnel SCALINGO_POSTGRESQL_URL
```

Lancer l'application (les paramètres sont documentés à l'exécution):
```bash
$ metabase_scan 'postgres://xxx:yyy@host:port/dbname' --dashboard-ids 3 4
```
