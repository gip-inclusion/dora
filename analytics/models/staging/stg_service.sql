WITH src AS (
    SELECT * FROM {{ source('dora', 'services_service') }}
    WHERE is_model IS FALSE
),

services AS (
    SELECT
        src.{{ dbt_utils.star(relation_alias=src, from=source('dora', 'services_service'), except=['geom']) }},
        ST_Y(CAST(src.geom AS geometry)) AS latitude,
        ST_X(CAST(src.geom AS geometry)) AS longitude,
        CASE
            WHEN
                src.modification_date + '240 days' <= NOW()
                AND src.status = 'PUBLISHED'
                THEN 'REQUIRED'
            WHEN
                src.modification_date + '180 days' <= NOW()
                AND src.status = 'PUBLISHED'
                THEN 'NEEDED'
            ELSE 'NOT_NEEDED'
        END                              AS update_status
        -- TODO(jbuget) : A documenter !
    FROM src
),

final AS (
    SELECT
        services.*,
        CONCAT('https://dora.inclusion.beta.gouv.fr/services/', services.slug) AS dora_url
    FROM services
)

SELECT * FROM final
