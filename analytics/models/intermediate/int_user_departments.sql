WITH users AS (

    SELECT *
    FROM {{ ref('stg_user') }}

),

final AS (

    SELECT DISTINCT
        users.id                              AS user_id,
        TRIM(unnested_departments.department) AS department
    FROM users
    CROSS JOIN LATERAL UNNEST(users.departments) AS unnested_departments (department)
    WHERE TRIM(unnested_departments.department) <> ''

)

SELECT *
FROM final
