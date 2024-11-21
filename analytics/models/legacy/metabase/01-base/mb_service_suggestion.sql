WITH src AS (
    SELECT * FROM {{ source('dora', 'service_suggestions') }}
),

final AS (
    SELECT *
    FROM src
)

SELECT * FROM final
