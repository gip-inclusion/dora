WITH structures AS (
    SELECT * FROM {{ ref("stg_structure") }}
),

WITH services AS (
    SELECT * FROM {{ ref("int_service_structure") }}
),

SELECT
    structures.id,
    count(services.id)
FROM structures
LEFT JOIN services on structures.id = services.structure_id
GROUP BY structures.id