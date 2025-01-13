WITH orientations AS (
    SELECT * FROM {{ ref('stg_orientation') }}
),

users AS (
    SELECT * FROM {{ ref('stg_user') }}
),

services AS (
    SELECT * FROM {{ ref('int_service_structure') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='orientations', from=ref('stg_orientation'), prefix='orientation_') }},
        {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }},
        {{ dbt_utils.star(relation_alias='services', from=ref('int_service_structure')) }}
    FROM orientations
    INNER JOIN users ON orientations.prescriber_id = users.id
    INNER JOIN services ON orientations.service_id = services.service_id
)

SELECT * FROM final
