# dora-front

## Pré-requis

- Node.js
- npm
- GitGuardian

## Installation

###

- [Installer GitGuardian](https://docs.gitguardian.com/internal-repositories-monitoring/gg_shield/getting_started#step-2-install-ggshield-gitguardian-cli) ;
- Copier le fichier `.env-example` en `.env` ;
- Renseigner la variable `VITE_API_URL` dans le fichier `.env` ;
  - La valeur `"https://api.dora.incubateur.net"` permet de connecter le front sur la preprod et ainsi éviter une mise en place locale du back ;
- Renseigner la variable `GITGUARDIAN_API_KEY` avec une clé d'API générée sur GitGuardian.com.

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

## Dépannage

Lorsque je clique sur `Référencer un service`, la page est blanche et j'ai l'erreur `TypeError: error loading dynamically imported module` dans la console

> Cela est peut-être dû à une extension de navigateur qui bloque des contenus nécessaires au bon fonctionnement : https://github.com/sveltejs/kit/issues/3308#issuecomment-1149942109

## Organisation des fichiers

### routes

Chaque répertoire correspond à une route, selon la norme Svelkit, mais on a regroupé les fichiers statiques (documents légaux, etc.) dans le repertoire `(static)`, et les differents endpoints (fichiers robots.txt, sitemap.xml, etc.) dans le repertoire `(endpoints)`.

D'autres regroupements pourraient être envisagés, par exemple `services` et `modeles`, pour faciliter la réutilisation de code localement.

### lib

- `assets`: toutes les ressources (fontes, icones, images…)
- `components`
  - `display`: tous les composants génériques d'affichage (boutons, labels, etc.)
  - `forms`: composants dédiés à l'affichage et à la validation des formulaire
  - `hoc`: composants de hauts niveau
  - `inputs`: composants d'entrée (hors validation -- ils sont encapsulés dans le repertoire `/form/fields` si nécessaire)
    - `obsolete`: composants qui font doublon avec un autre. À nettoyer, et à ne pas utiliser!!
  - `specialized`: composants spécialisés, qui seraient plus à leur place directement dans `/routes`, mais utilisés par plusieurs routes.
- `requests`: s'occupent de l'interaction avec l'API. À terme toutes les requetes à l'API devraient être faites ici plutôt qu'inline.
- `utils`: utilitaires variés. Éviter des mettre des fonctions qui ne servent qu'à un seul endroit.
- `validation`: gestion de la validation des formulaires
  - `schema`: les schemas déterminent les règles de validation des differents formulaire, ainsi que certaines valeurs d'affichage par defaut.
- `env.ts`: gestion des variables d'environnement
- `types.ts`: liste des types typescript partagés.
