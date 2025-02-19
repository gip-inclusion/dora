WITH structures AS (
    SELECT * FROM {{ source('dora', 'structures_structure') }}
),


final AS (
    SELECT
        structures.*,
        CONCAT('https://dora.inclusion.beta.gouv.fr/structures/', structures.slug) AS dora_url
    FROM structures
)

SELECT * FROM final
WHERE NOT is_obsolete
