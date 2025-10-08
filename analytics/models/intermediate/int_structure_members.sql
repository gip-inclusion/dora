WITH users AS (
    SELECT * FROM {{ ref('stg_user') }}
),

structure AS (
    SELECT * FROM {{ ref('stg_structure') }}
),

member AS (
    SELECT * FROM {{ source('dora', 'structures_structuremember') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='users', from=ref('stg_user'), prefix='user_') }},
        {{ dbt_utils.star(relation_alias='structure', from=ref('stg_structure'), prefix='structure_') }}
    FROM member
    INNER JOIN structure ON member.structure_id = structure.id
    INNER JOIN users ON member.user_id = users.id
)

SELECT * FROM final
