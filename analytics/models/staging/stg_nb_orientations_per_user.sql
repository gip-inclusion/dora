SELECT
    prescriber_id,
    MAX(creation_date) AS last_orientation_date,
    COUNT(*)           AS total_orientations
FROM {{ ref('stg_orientation') }}
WHERE prescriber_id IS NOT NULL
GROUP BY prescriber_id
