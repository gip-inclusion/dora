WITH search AS (
    SELECT * FROM {{ source('dora', 'search_views') }}
    WHERE
        is_staff IS FALSE
        AND is_manager IS FALSE
),

final AS (
    SELECT
        category.label            AS category,
        search.department,
        ss.label,
        COUNT(DISTINCT search.id) AS count
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
    GROUP BY
        category.label,
        search.department,
        ss.label
)

SELECT * FROM final
