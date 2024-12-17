WITH search AS (
    SELECT * FROM {{ source('dora', 'stats_searchview') }}
    WHERE
        is_staff IS FALSE
        AND is_manager IS FALSE
),

final AS (
    SELECT
        search.department,
        ss.label,
        TO_CHAR(search.date, 'YYYY-MM') AS month_year,
        COUNT(DISTINCT search.id)       AS count
    FROM search
    LEFT JOIN
        {{ source('dora', 'stats_searchview_categories') }} AS svc
        ON search.id = svc.searchview_id
    LEFT JOIN
        {{ source('dora', 'services_servicecategory') }} AS category
        ON svc.servicecategory_id = category.id
    LEFT JOIN
        {{ source('dora', 'structures_structuremember') }} AS member
        ON search.user_id = member.user_id
    -- les 2 JOINs suivants devraient etre directement dans mb_structure
    LEFT JOIN {{ ref('mb_structure') }} AS structure
        ON member.structure_id = structure.id
    LEFT JOIN
        {{ source('dora', 'structures_structure_national_labels') }} AS ssnl
        ON structure.id = ssnl.structure_id
    LEFT JOIN
        {{ source('dora', 'structures_structurenationallabel') }} AS ss
        ON ssnl.structurenationallabel_id = ss.id
    GROUP BY
        TO_CHAR(search.date, 'YYYY-MM'),
        search.department,
        ss.label
)

SELECT * FROM final
