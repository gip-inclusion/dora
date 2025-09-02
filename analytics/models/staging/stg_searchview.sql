WITH events AS (
    SELECT * FROM {{ source('dora', 'stats_searchview') }}
),

final AS (
    SELECT * FROM events
    WHERE
        CAST(date AS DATE) >= '2024-01-01'
        AND is_staff IS FALSE
)

SELECT * FROM final
