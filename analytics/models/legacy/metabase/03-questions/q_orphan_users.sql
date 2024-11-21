WITH orphaned_users AS (
    SELECT * FROM {{ ref('mb_user') }}
    WHERE
        NOT is_staff
        AND id NOT IN (SELECT m.user_id FROM {{ source('dora', 'members') }} AS m)
        AND id NOT IN (SELECT pm.user_id FROM {{ source('dora', 'putative_members') }} AS pm)
        AND id NOT IN (SELECT u."ID utilisateur" FROM {{ ref('q_users_before_ic') }} AS u)
),

final AS (
    SELECT
        mu.id                         AS "ID utilisateur",
        mu.email                      AS "E-mail",
        mu.first_name                 AS "Nom",
        mu.last_name                  AS "Prénom",
        mu.is_valid                   AS "E-mail validé",
        mu.date_joined                AS "Date de création",
        mu.last_login                 AS "Dernière connexion",
        CASE
            WHEN mu.date_joined > NOW() - interval '24 months' THEN FALSE
            WHEN mu.last_login IS NULL THEN TRUE
            ELSE mu.last_login < NOW() - interval '24 months'
        END                           AS "Compte inactif",
        mu.ic_id IS NOT NULL          AS "Inscrit IC",
        mu.date_joined < '2022-10-03' AS "Créé avant MEP IC"
    FROM orphaned_users AS mu
    ORDER BY mu.date_joined DESC
)

SELECT * FROM final
