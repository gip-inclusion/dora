SELECT
        services.*
FROM
        {{ source('dora', 'services_service') }} as services
WHERE is_model is TRUE