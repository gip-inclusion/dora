-- Décompte des recherches effectuées par des utilisateurs connectés :
-- non-gestionnaire, 
-- non-membre de l'équipe, 
-- et non-offreur seulement. 

WITH src AS (
    SELECT * FROM {{ source('dora', 'search_views') }}
    WHERE
        is_logged IS TRUE
        AND user_kind != 'offreur'
        AND is_manager IS FALSE
        AND is_staff IS FALSE
),

final AS (
    SELECT
        anonymous_user_hash,
        DATE_PART('doy', date)   AS jour,
        DATE_PART('week', date)  AS semaine,
        DATE_PART('month', date) AS mois,
        DATE_PART('year', date)  AS annee,
        COUNT(*)                 AS nb
    FROM src
    GROUP BY
        anonymous_user_hash,
        jour,
        semaine,
        mois,
        annee
    ORDER BY annee ASC, jour ASC, nb DESC
)

SELECT * FROM final
