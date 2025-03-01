
# 001 – Migrer tout le code DORA vers une mono-repository

Date : 2024-10-23

## État

Validé

## Contexte

Historiquement, le code de DORA est réparti entre 2 entrepôts de données : 

- [dora-back](https://github.com/gip-inclusion/dora-back) : la partie back-end, la plus historique, API, admin Django, gestion de la base de données, outillage d’exploitation
- [dora-front](https://github.com/gip-inclusion/dora-front) : la partie front-end, application Sveltekit

Ce découpage ne présente aucun réel avantage au quotidien. Ce pourrait être le cas si l’un ou l’autre *repository* était une lib indépendante réutilisable / réutilisée, ou un module / composant ultra spécifique ou particiulier. Ce n’est pas le cas ici.

A contrario, il présente plusieurs (petits) inconvénients ou (pertites) conséquences négatives :

- complique (un peu) l’installation du poste et la prise en main du projet pour un nouveau dev
- complique la tenue d’un CHANGELOG → de fait, il n’y en a pas
- complique la gestion de version (i.e. *releases*)→ de fait, il n’y en a pas
- oblige de créer plusieurs PR (et de jongler avec) pour une même *user story*
- empêche (ou la complexifie trop) la mise en place d’un mécanisme de *review app* automatique (application de recette jetable)

## Décision

Nous décidons de migrer et rassembler les 2 entrepôts de code dans un même endroit.

Il se trouve qu’il existe un 3ème repository – [gip-inclusion/dora](https://github.com/gip-inclusion/dora) – qui n’est qu’un pointeur vers les 2 autres. Nous décidons de réintégrer les 2 repositories dans celui-ci.

## Conséquences

Nous nous attendons à simplifier l’architecture / infrastructure ainsi que la prise en main du code, tout en facilitant la mise en œuvre d’outils d’exploitation avancés (CHANGELOG, SECURITY, releasing / versionning, gestion des PR / tickets, etc.).

## Mise en œuvre

Une copie basique des répertoires `dora-back` et `dora-front` engendrerait la perte de l'historique Git, ce qui est toujours dommage, surtout quand un soin et des efforts véritables y ont été consacré. Il est tout à fait possible d'internaliser des repositories tout en conserant l'historique (ex : [cet article](https://medium.com/@chris_72272/keeping-git-history-when-converting-multiple-repos-into-a-monorepo-97641744d928)). Il faudra bien en tenir compte en amont et pendant l'opération de migration.


**Avant**

- [X]  [GitHub] Fermer (intégrer ou archiver) toutes les PR actives pour les 2 repositories
- [X]  [Doc] Ajouter un fichier [INSTALL.md](http://INSTALL.md) ou modifier le README du repo dora
- [ ]  [Code] Prévoir des fichiers .*ignore intelligemment mutualisés
- [X]  [Organisation] Prévoir la date d’exécution

**Pendant**

- [X]  [GitHub] Copier chacun des 2 repo (”front” et “back”) dans le repo central “dora”
- [X]  [GitHub Actions] Retravailler la CI pour faire 2 jobs (front et back)
- [X]  [Scalingo] Modifier le link des apps (front + back ; prod + staging)
- [X]  [Scalingo] ajouter pour chacun la bonne variable `PROJECT_DIR` qui va bien

**Après**
- [X] [Ops] S'assurer que la plateforme (front et back) est OK
- [ ] [Doc] Mettre à jour la documentation pour déployer en production