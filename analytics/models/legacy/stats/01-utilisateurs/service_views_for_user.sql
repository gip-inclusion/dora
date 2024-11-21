-- Décompte des vues de service par utilisateur connecté : 
-- non-gestionnaire, 
-- non-membre de l'équipe, 
-- pas porté par une structure dont l'utilisateur est membre,
-- et non-offreur seulement. 

WITH src AS (
    SELECT * FROM {{ source('dora', 'service_views') }}
    WHERE
        is_logged IS TRUE
        AND user_kind != 'offreur'
        AND is_manager IS FALSE
        AND is_staff IS FALSE
),

non_members AS (
    SELECT * FROM src
    -- l'utilisateur ne visualise pas un service des structures dont il est membre
    WHERE NOT EXISTS (
        SELECT 1
        FROM structures_structuremember AS m
        WHERE
            m.user_id = src.user_id
            AND m.structure_id = src.structure_id
    )
),


final AS (
    SELECT
        anonymous_user_hash,
        DATE_PART('doy', date)   AS jour,
        DATE_PART('week', date)  AS semaine,
        DATE_PART('month', date) AS mois,
        DATE_PART('year', date)  AS annee,
        COUNT(*)                 AS nb
    FROM non_members
    GROUP BY
        anonymous_user_hash,
        jour,
        semaine,
        mois,
        annee
    ORDER BY annee ASC, jour ASC, nb DESC
)

SELECT * FROM final
