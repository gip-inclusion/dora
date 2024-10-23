drop table if exists mb_mobilisationevent_all;

create table mb_mobilisationevent_all as
select
    (select 'di-'::text || stats_dimobilisationevent.id) as id,
    stats_dimobilisationevent.path,
    stats_dimobilisationevent.date,
    stats_dimobilisationevent.anonymous_user_hash,
    stats_dimobilisationevent.is_logged,
    stats_dimobilisationevent.is_staff,
    stats_dimobilisationevent.is_manager,
    stats_dimobilisationevent.is_an_admin,
    (select false
    )                                                    as is_structure_admin,
    (select false
    )                                                    as is_structure_member,
    stats_dimobilisationevent.user_kind,
    stats_dimobilisationevent.structure_department,
    stats_dimobilisationevent.user_id,
    (select true)                                        as is_di
from
    stats_dimobilisationevent
union
select
    (select 'dora-'::text || stats_mobilisationevent.id) as id,
    stats_mobilisationevent.path,
    stats_mobilisationevent.date,
    stats_mobilisationevent.anonymous_user_hash,
    stats_mobilisationevent.is_logged,
    stats_mobilisationevent.is_staff,
    stats_mobilisationevent.is_manager,
    stats_mobilisationevent.is_an_admin,
    stats_mobilisationevent.is_structure_admin,
    stats_mobilisationevent.is_structure_member,
    stats_mobilisationevent.user_kind,
    stats_mobilisationevent.structure_department,
    stats_mobilisationevent.user_id,
    (select false)                                       as is_di
from
    stats_mobilisationevent;


alter table mb_mobilisationevent_all add primary key (id);
