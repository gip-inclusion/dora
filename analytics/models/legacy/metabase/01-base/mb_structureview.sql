WITH src AS (
    SELECT * FROM {{ source('dora', 'structure_views') }}
),

final AS (
    SELECT
        id,
        path,
        date,
        anonymous_user_hash,
        is_logged,
        is_staff,
        is_manager,
        is_an_admin,
        user_kind,
        structure_department,
        structure_id,
        structure_city_code,
        user_id,
        structure_source
    FROM src
)

SELECT * FROM final
