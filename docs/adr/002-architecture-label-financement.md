# 002 – Architecture des labels de financement

Date : 2024-10-30

## État

Validé

## Contexte

Certains services sont financés par des organismes publics. À ce titre, nous voulons :

- afficher un label de financement sur la fiche service, avec le nom de l'organisme financeur ;
- filtrer les résultats de recherche par financement ;
- établir des statistiques sur les affichages et mobilisations des services financés.

### Expérimentation

Nous avons réalisé une expérimentation avec implémentation purement _front-end_ pour deux financements :

- Conseil départemental de l’Aveyron ;
- Conseil départemental de la Drôme.

Un fichier JSON contient les données structurées relatives à chacun de ces financements :

- numéro de département (pour pouvoir afficher ou non le filtre en fonction du département de recherche) ;
- nom de l'organisme (affiché comme filtre) ;
- libellé (affiché sur la fiche service) ;
- liste des slugs des services financés (pour les identifier).

Afin de ne pas afficher des filtres inutiles sur la page des résultats de recherche, on affiche les filtres correspondant au département de la ville de recherche.

### Limites de l'expérimentation

Cette implémentation _front-end_ remplit bien les objectifs de filtrage et d'affichage du label de financement, mais pas celui de possibilité d'établir des statistiques. Il nous faut donc une implémentation _back-end_ avec stockage en base de données.

Les deux premiers types de financement sont liés à un département, mais les types de financements qu'on supportera à l'avenir peuvent être liés à d'autres types de collectivité territoriale... ou aucun en particulier ! Cela ne permet donc pas une implémentation unifiée pour les critères d'affichage des filtre.

De plus, la recherche se fait sur un rayon de 50 km. Les résultats ne sont donc pas nécessairement circonscrits à une collectivité territoriale unique, compliquant la logique d'affichage des filtres.

Enfin, on veut que les non-développeurs soient autonomes sur la gestion des labels de financement.

## Décision

Nous décidons d'une implémentation _back-end_ simple, où les labels de financement ne sont pas associés à une collectivité territoriale dans le modèle de données.

Ainsi, notre modèle de label de financement ne comportera que les champs suivants :

- Nom ;
- Relation plusieurs-à-plusieurs avec des services.

Nous décidons également que l'implémentation _front-end_ sera simple et unifiée.

Ainsi, les filtres affichés dépendront des résultats de recherche, et non pas des critères de recherche.

L'affichage des labels de financement sur la fiche service sera sous forme de liste.

## Conséquences

L'implémentation sera simple et adaptée à un grand nombre de cas de figure. Si des besoins supplémentaires devaient se présenter, on devrait pouvoir les implémenter facilement autour de cette architecture de base.

Avec l'exemple du financement par le conseil départemental de la Drôme, on aura les changements suivants par rapport à l'expérimentation purement _front-end_.

**Page des résultats de recherche :** le filtre ne s'affichera pas si la recherche se fait sur une ville de la Drôme, mais si au moins un résultat de recherche est associé au label de financement du département. On pourra ainsi avoir des recherches dans une ville de la Drôme qui ne fait ressortir aucun service financé par le département, auquel cas le filtre ne sera pas affiché. Mais on pourra aussi avoir des recherches dans une ville hors mais proche de la Drôme qui fait ressortir un service financé par le département de la Drôme, auquel cas le filtre sera affiché.

**Fiche service :** Le nom du filtre sur la page de résultats de recherche et le nom du label de financement sur la fiche service sera un seul et même libellé. On pourra par exemple lire sur la fiche : « Ce service est financé par : Conseil départemental de la Drôme ».
