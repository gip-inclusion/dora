# dora-front

## Pré-requis

- Node.js
- npm

## Installation

- Renommer le fichier `.env-example` en `.env`
- Renseigner la variable `VITE_API_URL` dans le fichier `.env`.
  - La valeur `"https://api.dora.incubateur.net"` permet de connecter le font sur la preprod et ainsi éviter une mise en place locale du back

```bash
# Installer les dépendances
npm install
```

## Développement

```bash
# Lancer un serveur de développement accessible sur localhost:3000
npm run dev
```

### Testing - e2e

Merci de vous reporter au README : [./e2e/README.md](./e2e/README.md).

## Contribution

```bash
# Installer les hooks de pre-commit
npm run prepare
```

- [Installer GitGuardian](https://docs.gitguardian.com/internal-repositories-monitoring/gg_shield/getting_started#step-2-install-ggshield-gitguardian-cli).
- Ajouter la clé d'API dans une variable d'environnement du shell `export GITGUARDIAN_API_KEY='**********'`.

## Dépannage

Lorsque je clique sur `Référencer un service`, la page est blanche et j'ai l'erreur `TypeError: error loading dynamically imported module` dans la console

> Cela est peut-être dû à une extension de navigateur qui bloque des contenus nécessaires au bon fonctionnement : https://github.com/sveltejs/kit/issues/3308#issuecomment-1149942109
