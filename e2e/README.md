# Commandes disponibles

`npm run test-e2e` : lance les tests en mode headless
`npm run test-e2e-debug` : lance les tests en liaison avec avec le Playwright Inspector, permettant de faire du pas-à-pas : https://playwright.dev/docs/debug

# Philosophie des tests

## Organisation du dossier `e2e`

Dossier `tests` contient les tests de l'application : par page / par scénario...

Dossier `pages` contient pour chaque page :

- son URL ou une fonction pour générer l'URL
- ses différents sélecteurs
- différentes fonction d'aide (remplissage d'un formulaire, récupération et formatages d'éléments de la page...)

Dossier `mocks` contient des données de réponses de requête HTTP en vue de les mocker avec `page.route`

## Priviligégier les sélecteurs et les fonctions d'aide

Autant que possible, il est conseillé d'utiliser, ajouter et améliorer les fonctions d'aide et les sélecteurs pour chaque page (dans le dossier `pages`).
Cela dans le but de faciliter la maintenance des tests e2e si une interaction ou un sélecteur devaient changer.

# Erreurs communes

Malheureusement, Playwright peut s'avérer peu explicite en cas d'erreurs...

Voici quelques cas rencontrés :

## Timeout lors de l'utilisation `route.fulfill`

Vérifiez que ne renvoyez bien un contenu de type `string` dans la propriété `body` de `route.fulfill`.

## Erreur : `Unexpected reserved word` sans plus de contexte

Un `await` a sûrement été utilisé sans un `async` dans la fonction.
