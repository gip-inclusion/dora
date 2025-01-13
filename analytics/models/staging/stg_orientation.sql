--         q.id=993 q.source_table='orientations_orientation' q.inception_level=0
--                 JOIN on mb_service
--                 JOIN on services_service_funding_labels
--                 JOIN on services_fundinglabel
-- 


-- ou une autre table dérivées jointe     avec mb_structuremember

--         q.id=948 q.source_table='mb_serviceview_all' q.inception_level=4
--                 JOIN on structures_structuremember
--                 JOIN on mb_structure
--                 JOIN on mb_user

WITH orientations AS (
    SELECT * FROM {{ source('dora', 'orientations_orientation') }}
),

final AS (
    SELECT * FROM orientations
    WHERE CAST(creation_date AS DATE) >= '2024-07-01'
)

SELECT * FROM final
