WITH src AS (
    SELECT * FROM {{ ref('mb_all_service') }}
    WHERE is_model IS FALSE
),

final AS (
    SELECT
        *,
        CONCAT('https://dora.inclusion.beta.gouv.fr/services/', slug) AS dora_url
    FROM src
)

SELECT * FROM final
