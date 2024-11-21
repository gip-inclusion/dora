WITH search AS (
    SELECT * FROM {{ source('dora', 'search_views') }}
    WHERE
        date >= NOW() - INTERVAL '30 days'
        AND is_staff IS FALSE
        AND is_manager IS FALSE
),

final AS (
    SELECT
        search.id,
        search.path,
        search.date,
        search.num_results,
        search.department,
        ss.label
    FROM search
    LEFT JOIN
        {{ source('dora', 'searchview_categories') }} AS svc
        ON search.id = svc.searchview_id
    LEFT JOIN
        {{ source('dora', 'service_categories') }} AS category
        ON svc.servicecategory_id = category.id
    LEFT JOIN
        {{ source('dora', 'members') }} AS member
        ON search.user_id = member.user_id
    LEFT JOIN {{ ref('mb_structure') }} AS structure
        ON member.structure_id = structure.id
    LEFT JOIN
        {{ source('dora', 'structure_labels') }} AS ssnl
        ON structure.id = ssnl.structure_id
    LEFT JOIN
        {{ source('dora', 'national_labels') }} AS ss
        ON ssnl.structurenationallabel_id = ss.id
)

SELECT * FROM final
