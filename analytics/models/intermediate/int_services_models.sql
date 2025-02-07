SELECT
    models.id     as model_id,
    models.name   as model_name,
    services.id   as service_id,
    structures.id as structure_id,
    structures.name,
    structures.department,
    structures.postal_code,
    structures.email,
    structures.phone
FROM
    {{ ref('stg_services_models') }} as models
LEFT JOIN
    {{ source('dora', 'services_service') }} as services
    ON models.id = services.model_id
LEFT JOIN
    {{ ref('stg_structure') }} as structures
    ON models.structure_id = structures.id