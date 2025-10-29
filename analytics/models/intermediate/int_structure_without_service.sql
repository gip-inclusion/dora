WITH structures AS (
    SELECT
        id,
        siret,
        name,
        department,
        typology
    FROM {{ ref("stg_structure") }}
),

services AS (
    SELECT structure_id FROM {{ ref("int_service_structure") }}
)

SELECT
    structures.id,
    structures.siret,
    structures.name,
    structures.department,
    structures.typology
FROM structures
WHERE NOT EXISTS (SELECT 1 FROM services WHERE services.structure_id = structures.id)
