WITH src AS (
    SELECT * FROM {{ source('dora', 'search_views') }}
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
        department,
        city_code,
        num_results,
        user_id,
        num_di_results,
        num_di_results_top10,
        results_slugs_top10
    FROM src
)

SELECT * FROM final
