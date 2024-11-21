WITH final AS (
    SELECT
        "ID utilisateur",
        "Nom",
        "Prénom",
        "E-mail",
        "E-mail validé",
        "Date de création",
        "Dernière connexion",
        "Nom de la structure",
        "URL Dora",
        "SLUG",
        "Département",
        "Date d'invitation",
        "Invitation en tant qu'admin",
        "Compte inactif",
        "Nombre d'admins dans la structure",
        "Premier admin de la structure",
        "Membre d'autres structures"
    FROM {{ ref('mb_putative_members') }}
    WHERE NOT "E-mail validé" AND "Invitation par un admin"
)

SELECT * FROM final
