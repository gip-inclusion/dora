WITH events AS (
    SELECT * FROM {{ ref('stg_serviceview') }}
),

services AS (
    SELECT * FROM {{ ref('int_service_structure') }}
),

users AS (
    SELECT * FROM {{ ref('stg_user') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='events', from=ref('stg_serviceview'), prefix='event_') }},
        {{ dbt_utils.star(relation_alias='services', from=ref('int_service_structure')) }},
        {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }}
    FROM events
    INNER JOIN services ON CAST(services.service_id AS TEXT) = events.service_id
    LEFT JOIN users ON events.user_id = users.id
)

SELECT * FROM final
