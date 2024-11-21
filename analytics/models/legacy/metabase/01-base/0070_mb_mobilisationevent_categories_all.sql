drop table if exists mb_mobilisationevent_categories_all;

create table mb_mobilisationevent_categories_all as
select
    (
        select
            'di-'::text
            || stats_dimobilisationevent_categories.dimobilisationevent_id
    ) as mobilisationevent_id,
    stats_dimobilisationevent_categories.servicecategory_id
from
    stats_dimobilisationevent_categories
union
select
    (
        select
            'dora-'::text
            || stats_mobilisationevent_categories.mobilisationevent_id
    ) as mobilisationevent_id,
    stats_mobilisationevent_categories.servicecategory_id
from
    stats_mobilisationevent_categories;
