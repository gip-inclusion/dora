WITH events AS (
    SELECT * FROM {{ ref('stg_pageview') }}
),

users AS (
    SELECT * FROM {{ ref('stg_user') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='events', from=ref('stg_pageview'), prefix='event_') }},
        {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }}
    FROM events
    INNER JOIN users ON events.user_id = users.id
)

SELECT * FROM final
