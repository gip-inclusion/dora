WITH structures AS (
    SELECT * FROM {{ source('dora', 'structures_structure') }}
),


final AS (
    SELECT
        structures.*,
        'dora--' || structures.id as id_jointure_di,
        CONCAT('https://dora.inclusion.gouv.fr/structures/', structures.slug) AS dora_url
    FROM structures
)

SELECT * FROM final
WHERE NOT is_obsolete
