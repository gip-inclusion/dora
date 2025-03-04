SELECT
    {{ dbt_utils.star(relation_alias='orientations', from=ref('stg_orientation'), prefix='orientation_') }},
    {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }},
    {{ dbt_utils.star(relation_alias='services', from=ref('int_service_structure')) }}
FROM {{ ref('stg_orientation') }} AS orientations
INNER JOIN {{ ref('stg_user') }} AS users
    ON orientations.prescriber_id = users.id
INNER JOIN {{ ref('int_service_structure') }} AS services
    ON orientations.service_id = services.service_id
