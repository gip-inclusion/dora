SELECT services.*
FROM
    {{ source('dora', 'services_service') }} AS services
WHERE services.is_model IS TRUE
