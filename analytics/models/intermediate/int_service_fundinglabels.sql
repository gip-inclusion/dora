WITH services AS (
    SELECT * FROM {{ ref("int_service_structure") }}
),

fundinglabel_pairs AS (
    SELECT * FROM {{ source('dora', 'services_service_funding_labels') }}
),

fundinglabels AS (
    SELECT * FROM {{ source('dora', 'services_fundinglabel') }}
),

final AS (
    SELECT
        services.*,
        fundinglabels.label AS fundinglabel_name,
        fundinglabels.value AS fundinglabel_label
    FROM services
    LEFT JOIN fundinglabel_pairs ON services.service_id = fundinglabel_pairs.service_id
    LEFT JOIN fundinglabels ON fundinglabel_pairs.fundinglabel_id = fundinglabels.id
)

SELECT * FROM final
