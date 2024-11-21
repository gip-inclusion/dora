WITH src AS (
    SELECT * FROM {{ ref('mb_all_service') }}
    WHERE is_model IS TRUE
),

final AS (
    SELECT
        id,
        name,
        short_desc,
        full_desc,
        is_cumulative,
        fee_details,
        beneficiaries_access_modes_other,
        coach_orientation_modes_other,
        forms,
        recurrence,
        suspension_date,
        creation_date,
        modification_date,
        creator_id,
        last_editor_id,
        structure_id,
        slug,
        online_form,
        qpv_or_zrr,
        sync_checksum,
        fee_condition_id,
        CONCAT('https://dora.inclusion.beta.gouv.fr/modeles/', slug) AS dora_url
    FROM src
)

SELECT * FROM final
