-- noqa: disable=LT05
drop table if exists mb_all_service cascade;

create table mb_all_service as
select
    services_service.id,
    services_service.name,
    services_service.short_desc,
    services_service.full_desc,
    services_service.is_cumulative,
    services_service.fee_details,
    services_service.beneficiaries_access_modes_other,
    services_service.coach_orientation_modes_other,
    services_service.forms,
    services_service.contact_name,
    services_service.contact_phone,
    services_service.contact_email,
    services_service.is_contact_info_public,
    services_service.remote_url,
    services_service.address1,
    services_service.address2,
    services_service.postal_code,
    services_service.city_code,
    services_service.city,
    services_service.recurrence,
    services_service.suspension_date,
    services_service.creation_date,
    services_service.modification_date,
    services_service.creator_id,
    services_service.last_editor_id,
    services_service.structure_id,
    services_service.slug,
    services_service.online_form,
    services_service.publication_date,
    services_service.diffusion_zone_details,
    services_service.diffusion_zone_type,
    services_service.qpv_or_zrr,
    services_service.is_model,
    services_service.model_id,
    services_service.last_sync_checksum,
    services_service.sync_checksum,
    services_service.status,
    services_service.moderation_date,
    services_service.moderation_status,
    services_service.fee_condition_id,
    services_service.use_inclusion_numerique_scheme,
    services_service.source_id,
    services_service.data_inclusion_id,
    services_service.data_inclusion_source,
    (select st_y((services_service.geom)::geometry) as st_y) as latitude,
    (select st_x((services_service.geom)::geometry) as st_x) as longitude,
    case
        when
            services_service.modification_date + '240 days' <= now()
            and services_service.status = 'PUBLISHED'
            then 'REQUIRED'
        when
            services_service.modification_date + '180 days' <= now()
            and services_service.status = 'PUBLISHED'
            then 'NEEDED'
        else 'NOT_NEEDED'
    end                                                      as update_status
from services_service;

alter table mb_all_service add primary key (id);
