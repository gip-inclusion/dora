# Dora

> Faciliter la vie des personnes en insertion et de celles et ceux qui les accompagnent

- [Backend](back/README.md)
- [Frontend](front/README.md)

## Review apps

Chaque PR peut avoir sa paire de review apps Scalingo (région `osc-fr1`), créées à la demande à partir des apps parentes `dora-back-review` et `dora-front-review` :

```bash
tools/create-review-apps.sh <numéro de PR>
```

- `dora-front-review-pr<N>` appelle l'API de `dora-back-review-pr<N>` (voir `front/scalingo.json` et `back/scalingo.json`).
- Les review apps back partagent la base de données de `dora-back-review`. Le process `clock` de cette app parente (`tools/clock.sh`) la restaure chaque nuit à 2 h UTC depuis la dernière sauvegarde du staging (`tools/reset-database.sh`).
- Les review apps n'ont pas de tâches planifiées : `back/bin/post_compile` supprime `cron.json` quand `ENVIRONMENT=review` (Scalingo limite le nombre de tâches cron par app).
- Les review apps sont supprimées automatiquement au merge de la PR.

## Livraison

La livraison crée un tag de version, puis déploie son archive sur les apps Scalingo back et front :

```bash
export SCALINGO_REGION=osc-fr1 SCALINGO_BACK_APP=<app back> SCALINGO_FRONT_APP=<app front>
tools/release.sh major|minor|patch      # depuis main
tools/release.sh hotfix <branche>       # depuis une branche de correctif
```

Le script calcule la version à partir du dernier tag (`hotfix` incrémente le patch), et ne fait rien si le dernier commit de la branche source porte déjà ce tag. Il nécessite le CLI Scalingo et un accès collaborateur aux deux apps.
