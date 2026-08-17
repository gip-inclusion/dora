# Mots de passe

Les utilisateurs se connectent exclusivement par ProConnect. Seuls les utilisateurs `is_staff` peuvent se connecter via l'authentification Django à Django Admin.

En fonction de la façon dont a été créé l'utilisateur, le format du contenu du champ `password` peut varier :


| Valeur            | Origine                                                                                                                                                    |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `pbkdf2_sha256$…` | `set_password()` — inscription e-mail/mdp d'avant Inclusion Connect, superusers, création via l'admin                                                      |
| `!` + 40 car.     | `set_unusable_password()` via `create_user()` — ProConnect, invitations, import CSV. Cas nominal actuel                                                    |
| `""`              | `User.objects.create()` dans l'ancien callback Inclusion Connect (`dora/oidc/views.py` avant `fd909a5c`, 14/11/2024) — ne passait pas par `set_password()` |
| `!disabled`       | Chaîne d'anonymisation (`tools/datanymizer-config.yml:26`) + [data.inclusion@beta.gouv.fr](mailto:data.inclusion@beta.gouv.fr) en prod                     |


Une normalisation de valeurs du champ `password` a été faite en août 2026 afin que tous les utilisateurs normaux (non `is_staff`) aient une valeur au format `!` + 40 car.