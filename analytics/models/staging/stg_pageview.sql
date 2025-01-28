WITH events AS (
    SELECT * FROM {{ source('dora', 'stats_pageview') }}
),

final AS (
    SELECT * FROM events
    WHERE
        -- date discutée avec Chloé pour limiter la taille de la table
        CAST(date AS DATE) >= '2024-07-01'
        AND is_staff IS FALSE
)

SELECT * FROM final
