# Dora

> Faciliter la vie des personnes en insertion et de celles et ceux qui les accompagnent

- [Backend](back/README.md)
- [Frontend](front/README.md)

## Review apps

Chaque PR peut avoir sa paire de review apps Scalingo (région `osc-fr1`), créées à la demande à partir des apps parentes `dora-back-review-apps` et `dora-front-review-apps` (projet Scalingo `dora-staging`) :

```bash
tools/create-review-apps.sh <numéro de PR>
```

- `dora-front-review-apps-pr<N>` appelle l'API de `dora-back-review-apps-pr<N>` (voir `front/scalingo.json` et `back/scalingo.json`).
- Les review apps back partagent la base de données de `dora-back-review-apps`. Le process `clock` de cette app parente (`tools/clock.sh`) la restaure chaque nuit à 2 h UTC depuis la dernière sauvegarde du staging (`tools/reset-database.sh`).
- Les review apps n'ont pas de tâches planifiées : `back/bin/post_compile` supprime `cron.json` quand `ENVIRONMENT=review` (Scalingo limite le nombre de tâches cron par app).
- Les review apps sont supprimées automatiquement au merge de la PR.

## Livraison

La livraison crée un tag de version, puis déploie son archive sur les apps Scalingo back et front :

```bash
tools/release.sh major|minor|patch      # depuis main
tools/release.sh hotfix <branche>       # depuis une branche de correctif
```

Par défaut, le script cible la prod (`dora-back-prod` et `dora-front-prod`, région `osc-secnum-fr1`). Les variables d'environnement `SCALINGO_REGION`, `SCALINGO_BACK_APP` et `SCALINGO_FRONT_APP` permettent de cibler d'autres apps. Le script affiche la cible et demande confirmation avant de continuer.

Le script calcule la version à partir du dernier tag (`hotfix` incrémente le patch), et ne fait rien si le dernier commit de la branche source porte déjà ce tag. Il nécessite le CLI Scalingo et un accès collaborateur aux deux apps.
