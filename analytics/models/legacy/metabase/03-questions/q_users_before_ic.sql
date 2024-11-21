WITH users AS (
    SELECT * FROM {{ ref('mb_user') }}
    WHERE NOT is_staff
    -- adresse e-mail non validée
    AND NOT is_valid
    -- aucun rattachement en attente
    AND id NOT IN (SELECT pm.user_id FROM {{ source('dora', 'putative_members') }} AS pm)
    -- aucune connexion IC
    AND ic_id IS NULL
),

final AS (
    SELECT
        mu.id                           AS "ID utilisateur",
        mu.email                        AS "E-mail",
        mu.date_joined                  AS "Date de création",
        (
            CASE
                WHEN mu.date_joined > NOW() - interval '24 months' THEN FALSE
                WHEN mu.last_login IS NULL THEN TRUE
                ELSE mu.last_login < NOW() - interval '24 months'
            END
        )                               AS "Compte inactif",
        (mu.date_joined < '2022-10-03') AS "Créé avant IC"
    FROM users AS mu
    ORDER BY mu.date_joined DESC
)

SELECT * FROM final
