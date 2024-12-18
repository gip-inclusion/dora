WITH users AS (
    SELECT * FROM {{ ref('stg_user') }}
),

events AS (
    SELECT * FROM {{ ref('stg_mobilisationevent') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='events', from=ref('stg_mobilisationevent'), prefix='event_') }},
        {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }}
    FROM events
    INNER JOIN users ON events.user_id = users.id
)

SELECT * FROM final
