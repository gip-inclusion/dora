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
            WHEN status != 'PUBLISHED' THEN FALSE
            WHEN update_frequency = 'tous-les-mois' 
                AND modification_date + INTERVAL '1 month' <= NOW() THEN TRUE
            WHEN update_frequency = 'tous-les-3-mois'
                AND modification_date + INTERVAL '3 months' <= NOW() THEN TRUE
            WHEN update_frequency = 'tous-les-6-mois'
                AND modification_date + INTERVAL '6 months' <= NOW() THEN TRUE
            WHEN update_frequency = 'tous-les-12-mois'
                AND modification_date + INTERVAL '12 months' <= NOW() THEN TRUE
            WHEN update_frequency = 'tous-les-16-mois'
                AND modification_date + INTERVAL '16 months' <= NOW() THEN TRUE
            ELSE FALSE
        END AS update_needed
    FROM src
),

final AS (
    SELECT
        services.*,
        CONCAT('https://dora.inclusion.beta.gouv.fr/services/', services.slug) AS dora_url
    FROM services
)

SELECT * FROM final
