WITH users AS (
    SELECT * FROM {{ ref('mb_user') }}
    WHERE
        NOT is_staff
),

final AS (
    SELECT
        users.id                AS "ID utilisateur",
        users.first_name        AS "Nom",
        users.last_name         AS "Prénom",
        users.email             AS "E-mail",
        users.is_valid          AS "E-mail validé",
        users.date_joined       AS "Date de création",
        users.last_login        AS "Dernière connexion",
        structure.name          AS "Nom de la structure",
        structure.slug          AS "SLUG",
        structure.dora_url      AS "URL Dora",
        structure.department    AS "Département",
        member.creation_date    AS "Date d'invitation",
        member.is_admin         AS "Invitation en tant qu'admin",
        -- invité : l'utilisateur ne s'est pas rattaché lui-même à la structure 
        member.invited_by_admin AS "Invitation par un admin",
        (
            CASE
                WHEN users.date_joined > NOW() - interval '24 months' THEN FALSE
                WHEN users.last_login IS NULL THEN TRUE
                ELSE users.last_login < NOW() - interval '24 months'
            END
        )                       AS "Compte inactif",
        -- TODO: un refactor avec une table utilitaire pour éviter les jointures ?
        -- NOTE(vperron): oui, en haute priorité
        (
            SELECT COUNT(*)
            FROM {{ source('dora', 'members') }} AS ssm
            INNER JOIN {{ ref('mb_user') }} AS mu2 ON ssm.user_id = mu2.id AND mu2.is_valid
            WHERE ssm.is_admin AND ssm.structure_id = structure.id
        )                       AS "Nombre d'admins dans la structure",
        (
            member.is_admin
            AND (
                SELECT COUNT(*) = 0
                FROM {{ source('dora', 'members') }} AS ssm
                INNER JOIN {{ ref('mb_user') }} AS mu2 ON ssm.user_id = mu2.id AND mu2.is_valid
                WHERE
                    ssm.structure_id = member.structure_id
                    AND ssm.is_admin
            )
        )                       AS "Premier admin de la structure",
        (
            SELECT COUNT(*)
            FROM {{ source('dora', 'members') }} AS ss2
            WHERE
                ss2.user_id = users.id
        )                       AS "Membre d'autres structures"
    FROM users
    INNER JOIN {{ source('dora', 'putative_members') }} AS member ON users.id = member.user_id
    LEFT JOIN {{ ref('mb_structure') }} AS structure ON member.structure_id = structure.id
    ORDER BY users.date_joined DESC
)

SELECT * FROM final
