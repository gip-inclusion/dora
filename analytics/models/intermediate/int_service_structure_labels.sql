WITH services AS (
    SELECT * FROM {{ ref("stg_service") }}
),

structure AS (
    SELECT * FROM {{ ref("int_structure_national_labels") }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='services', from=ref("stg_service"), prefix='service_') }},
        {{ dbt_utils.star(relation_alias='structure', from=ref("int_structure_national_labels"), prefix='structure_') }}
    FROM services
    INNER JOIN structure ON services.structure_id = structure.structure_id
)

SELECT * FROM final
