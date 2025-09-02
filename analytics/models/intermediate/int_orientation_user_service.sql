SELECT
    {{ dbt_utils.star(relation_alias='orientations', from=ref('stg_orientation'), prefix='orientation_') }},
    {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }},
    {{ dbt_utils.star(relation_alias='services', from=ref('int_service_structure')) }}
FROM {{ ref('stg_orientation') }} AS orientations
-- left join pour considérer les orientations faites par des users supprimés
LEFT JOIN {{ ref('stg_user') }} AS users
    ON orientations.prescriber_id = users.id
-- left join pour considérer les cas suivants : 
-- orientations faites sur des services sans service_id (ont un di_service_id)
-- orientations faites sur des services non rattachés à une structure
LEFT JOIN {{ ref('int_service_structure') }} AS services
    ON orientations.service_id = services.service_id
