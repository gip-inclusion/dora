WITH structures AS (
    SELECT * FROM {{ ref("stg_structure") }}
),

national_label_pairs AS (
    SELECT * FROM {{ source('dora', 'structures_structure_national_labels') }}
),

national_labels AS (
    SELECT * FROM {{ source('dora', 'structures_structurenationallabel') }}
),

final AS (
    SELECT
        {{ dbt_utils.star(relation_alias='structures', from=ref('stg_structure'), prefix='structure_') }},
        national_labels.label           AS national_label_name,
        national_labels.value           AS national_label_code
    FROM structures
    LEFT JOIN national_label_pairs ON structures.id = national_label_pairs.structure_id
    LEFT JOIN national_labels ON national_label_pairs.structurenationallabel_id = national_labels.id
)

SELECT * FROM final
