WITH src AS (
    SELECT * FROM {{ source('dora', 'structures_structure') }}
),

final AS (
    SELECT
        *,
        CONCAT('https://dora.inclusion.beta.gouv.fr/structures/', slug) AS dora_url
    FROM src
)

SELECT * FROM final
