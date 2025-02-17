# Modèle de données DORA

## A propos 

Permet d'avoir un lien pour une visualisation détaillée du modèle (par ex. pour l'AIPD).

## Installation des dépendances 

Les dépendances nécessaires pour la génération sont dans le fichier de dépendances `requirements/dev.txt` :
- `django-extensions`
- `pygraphviz`

La configuration de `django-extensions` est présente dans le fichier `config/settings/dev.py`.

`pygraphviz` dépends de la librairies [Graphviz](https://www.graphviz.org/). 

Voir les directives d'installation pour les OS / distributions les plus courants en référence.

Pour rappel, l'installation des dépendances de `dev` se fait via `pip` :
```bash 
pip install -r requirements/dev.txt
```

## Génération

Depuis le répertoire de l'application `back`, exporté avec `django-extensions` via :


```bash
./manage.py graph_models -a -o ../docs/models/dora_model.png`

```

## Références 

- [django-extensions - génération de modèle](https://django-extensions.readthedocs.io/en/latest/graph_models.html)
- [Installation de Graphviz pour pygraphviz](https://pygraphviz.github.io/documentation/stable/install.html)

