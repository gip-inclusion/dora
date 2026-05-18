WITH users AS (

    SELECT *
    FROM {{ ref('stg_user') }}

),

final AS (

    SELECT DISTINCT
        users.id AS user_id,
        trim(unnested_departments.department) AS department
    FROM users
    CROSS JOIN LATERAL unnest(users.departments) AS unnested_departments(department)
    WHERE trim(unnested_departments.department) <> ''

)

SELECT *
FROM final
