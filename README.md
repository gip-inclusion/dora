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

Ce projet utilise [conventional-changelog](https://github.com/angular/angular/blob/master/CONTRIBUTING.md#-commit-message-format) pour les messages de commits. Pour un rédiger un message de commit formaté selon cette convention, utiliser la commande `npm run commit` au lieu de `git commit …`.
