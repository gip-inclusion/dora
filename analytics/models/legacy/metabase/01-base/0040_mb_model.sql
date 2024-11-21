drop view if exists mb_model;

create view mb_model as
select
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
    (
        select concat('https://dora.inclusion.beta.gouv.fr/modeles/', slug)
    ) as dora_url
from mb_all_service where is_model is true;
