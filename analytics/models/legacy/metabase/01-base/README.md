Ici toutes les définitions de tables et vues metabase anciennement maj via scripts shell.

Règles à avoir en tête :
* tout fichier est considéré comme une table ou vue qui sera DROP par le script
* de fait, il n'est pas possible d'avoir de fichiers avec juste de l'ajout de CONSTRAINTS ou d'INDEX ; il faut penser à reconstruire la table