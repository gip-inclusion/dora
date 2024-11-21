drop table if exists mb_serviceview_all;

create table mb_serviceview_all as
select
    (select 'di-'::text || disv.id) as id,
    disv.path,
    disv.date,
    disv.anonymous_user_hash,
    disv.is_logged,
    disv.is_staff,
    disv.is_manager,
    disv.is_an_admin,
    (select false)                  as is_structure_admin,
    (select false)                  as is_structure_member,
    disv.user_kind,
    disv.structure_department,
    disv.user_id,
    disv.source,
    (select false)                  as is_orientable,
    (select true)                   as is_di,
    disv.service_id::text,
    disv.structure_id,
    disv.service_name,
    disv.structure_name
from
    stats_diserviceview as disv
union
select
    (select 'dora-'::text || sv.id) as id,
    sv.path,
    sv.date,
    sv.anonymous_user_hash,
    sv.is_logged,
    sv.is_staff,
    sv.is_manager,
    sv.is_an_admin,
    sv.is_structure_admin,
    sv.is_structure_member,
    sv.user_kind,
    sv.structure_department,
    sv.user_id,
    sv.service_source               as source,
    sv.is_orientable,
    (select false)                  as is_di,
    sv.service_id::text,
    sv.structure_id::text,
    s.name                          as service_name,
    st.name                         as structure_name
from
    stats_serviceview as sv
left join services_service as s on sv.service_id = s.id
left join structures_structure as st on sv.structure_id = st.id;

alter table mb_serviceview_all add primary key (id);

-- Indexes
create index idx_mb_serviceview_all_structure_id
on mb_serviceview_all ("structure_id");

create index idx_mb_serviceview_all_user_id
on mb_serviceview_all ("user_id");

create index idx_mb_serviceview_all_is_staff_is_manager
on mb_serviceview_all ("is_staff", "is_manager");
