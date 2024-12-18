WITH services AS (
    SELECT * FROM {{ ref("stg_service") }}
),

structure AS (
    SELECT * FROM {{ ref("stg_structure") }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='services', from=ref("stg_service"), prefix='service_') }},
        {{ dbt_utils.star(relation_alias='structure', from=ref("stg_structure"), prefix='structure_') }}
    FROM services
    INNER JOIN structure ON services.structure_id = structure.id
)

SELECT * FROM final
