WITH services AS (
    SELECT * FROM {{ ref("int_service_structure") }}
),

categorie_pairs AS (
    SELECT * FROM {{ source('dora', 'services_service_categories') }}
),

categories AS (
    SELECT * FROM {{ source('dora', 'services_servicecategory') }}
),

final AS (
    SELECT
        services.*,
        categories.label AS category_name,
        categories.value AS category_label
    FROM services
    LEFT JOIN categorie_pairs ON services.service_id = categorie_pairs.service_id
    LEFT JOIN categories ON categorie_pairs.servicecategory_id = categories.id
)

SELECT * FROM final
