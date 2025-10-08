SELECT
    models.id     AS model_id,
    models.name   AS model_name,
    services.id   AS service_id,
    structures.id AS structure_id,
    structures.name,
    structures.department,
    structures.postal_code,
    structures.email,
    structures.phone
FROM
    {{ ref('stg_services_models') }} AS models
LEFT JOIN
    {{ source('dora', 'services_service') }} AS services
    ON models.id = services.model_id
LEFT JOIN
    {{ ref('stg_structure') }} AS structures
    ON models.structure_id = structures.id
