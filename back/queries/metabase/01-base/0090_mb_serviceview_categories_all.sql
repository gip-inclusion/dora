drop table if exists mb_serviceview_categories_all;


create table mb_serviceview_categories_all as
select
    (select 'di-'::text || dic.diserviceview_id) as serviceview_id,
    dic.servicecategory_id
from
    stats_diserviceview_categories as dic
union
select
    (select 'dora-'::text || svc.serviceview_id) as serviceview_id,
    svc.servicecategory_id
from
    stats_serviceview_categories as svc;
