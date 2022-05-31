# dora-front

## Pré-requis

- Node.js
- npm

## Installation

- Renommer le fichier `.env-example` en `.env`
- Renseigner la variable `VITE_API_URL` dans le fichier `.env`.

```bash
# Installer les dépendances
npm install
```

## Développement

```bash
# Lancer un serveur de développement accessible sur localhost:3000
npm run dev
```

## Contribution

```bash
# Installer les hooks de pre-commit
npm run prepare
```

- [Installer GitGuardian](https://docs.gitguardian.com/internal-repositories-monitoring/gg_shield/getting_started#step-2-install-ggshield-gitguardian-cli).
- Ajouter la clé d'API dans une variable d'environnement du shell `export GITGUARDIAN_API_KEY='**********'`.

### Suivi de version

Ce projet utilise [conventional-changelog](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) pour les messages de commits.

Pour un rédiger un message de commit formaté selon cette convention, utiliser la commande `npm run commit` (ou `npx cz`) au lieu de `git commit …`.

### Publier une nouvelle version (release)

Publier une nouvelle version consiste à :

- Mettre à jour le numéro de version
- Mettre à jour le fichier de changelog (automatiquement en fonction des messages de commits formatés)
- Ajouter un tag git avec le numéro de version
- Publier la nouvelle version sur Github

```bash
# Basculer sur la branche main
git checkout main

# Récupèrer la dernière version sur github
git pull --rebase origin main

# Publier une nouvelle version
npm run release
```

### Déployer en prod

```bash
# Basculer sur la branche release
git checkout release

# Inclure le contenu de la branche main (fast forward)
git merge main

# Pousser sur Github
git push origin release
```
