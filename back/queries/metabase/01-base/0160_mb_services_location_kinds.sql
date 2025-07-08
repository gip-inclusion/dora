drop table if exists mb_services_service_location_kinds;

create table mb_services_service_location_kinds as
select
    id,
    service_id,
    locationkind_id
from
    services_service_location_kinds;

alter table mb_services_service_location_kinds add primary key (id);

-- Indexes
create index idx_mb_services_service_location_kinds_service_id
on mb_services_service_location_kinds (service_id);

create index idx_mb_services_service_location_kinds_locationkind_id
on mb_services_service_location_kinds (locationkind_id);

create index idx_mb_services_service_location_kinds_service_locationkind
on mb_services_service_location_kinds (service_id, locationkind_id);
