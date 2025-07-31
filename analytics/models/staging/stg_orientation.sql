WITH orientations AS (
    SELECT * FROM {{ source('dora', 'orientations_orientation') }}
),

final AS (
    SELECT * FROM orientations
    -- date discutée avec Chloé pour limiter la taille de la table
    WHERE CAST(creation_date AS DATE) >= '2024-01-01'
)

SELECT * FROM final
