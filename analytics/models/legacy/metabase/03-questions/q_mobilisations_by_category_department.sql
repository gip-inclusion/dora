WITH mobilisation AS (
    SELECT * FROM {{ source('dora', 'stats_mobilisationevent') }}
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
        {{ source('dora', 'services_service_categories') }} AS svc_category
        ON mobilisation.service_id = svc_category.service_id
    LEFT JOIN
        {{ source('dora', 'services_servicecategory') }} AS category
        ON svc_category.servicecategory_id = category.id
    LEFT JOIN
        {{ source('dora', 'structures_structuremember') }} AS member
        ON mobilisation.user_id = member.user_id
    -- les 2 JOINs suivants devraient etre directement dans mb_structure
    LEFT JOIN {{ ref('mb_structure') }} AS structure
        ON member.structure_id = structure.id
    LEFT JOIN
        {{ source('dora', 'structures_structure_national_labels') }} AS ssnl
        ON structure.id = ssnl.structure_id
    LEFT JOIN
        {{ source('dora', 'structures_structurenationallabel') }} AS ss
        ON ssnl.structurenationallabel_id = ss.id
)

SELECT * FROM final
