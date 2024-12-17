WITH src AS (
    SELECT * FROM {{ source('dora', 'services_service') }}
),

tmp AS (
    SELECT
        src.id,
        src.name,
        src.short_desc,
        src.full_desc,
        src.is_cumulative,
        src.fee_details,
        src.beneficiaries_access_modes_other,
        src.coach_orientation_modes_other,
        src.forms,
        src.contact_name,
        src.contact_phone,
        src.contact_email,
        src.is_contact_info_public,
        src.remote_url,
        src.address1,
        src.address2,
        src.postal_code,
        src.city_code,
        src.city,
        src.recurrence,
        src.suspension_date,
        src.creation_date,
        src.modification_date,
        src.creator_id,
        src.last_editor_id,
        src.structure_id,
        src.slug,
        src.online_form,
        src.publication_date,
        src.diffusion_zone_details,
        src.diffusion_zone_type,
        src.qpv_or_zrr,
        src.is_model,
        src.model_id,
        src.last_sync_checksum,
        src.sync_checksum,
        src.status,
        src.moderation_date,
        src.moderation_status,
        src.fee_condition_id,
        src.use_inclusion_numerique_scheme,
        src.source_id,
        src.data_inclusion_id,
        src.data_inclusion_source,
        ST_Y(CAST(src.geom AS geometry)) AS latitude,
        ST_X(CAST(src.geom AS geometry)) AS longitude,
        CASE
            WHEN
                src.modification_date + '240 days' <= NOW()
                AND src.status = 'PUBLISHED'
                THEN 'REQUIRED'
            WHEN
                src.modification_date + '180 days' <= NOW()
                AND src.status = 'PUBLISHED'
                THEN 'NEEDED'
            ELSE 'NOT_NEEDED'
        END                              AS update_status
    FROM src
),

final AS (
    SELECT
        *,
        CONCAT('https://dora.inclusion.beta.gouv.fr/services/', slug) AS dora_url
    FROM tmp
    WHERE is_model IS FALSE
)

SELECT * FROM final
