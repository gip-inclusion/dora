WITH mobilisation AS (
    SELECT * FROM {{ source('dora', 'mobilisation_events') }}
    WHERE
        is_staff IS FALSE
        AND is_manager IS FALSE
        AND is_structure_member IS FALSE
        AND is_structure_admin IS FALSE
),

final AS (
    SELECT
        mobilisation.id,
        mobilisation.path,
        mobilisation.date,
        structure.department,
        ss.label,
        category.label AS category
    FROM mobilisation
    LEFT JOIN
        {{ source('dora', 'service_category_link') }} AS svc_category
        ON mobilisation.service_id = svc_category.service_id
    LEFT JOIN
        {{ source('dora', 'service_categories') }} AS category
        ON svc_category.servicecategory_id = category.id
    LEFT JOIN
        {{ source('dora', 'members') }} AS member
        ON mobilisation.user_id = member.user_id
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
