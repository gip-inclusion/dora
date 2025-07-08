drop table if exists mb_services_locationkind;

create table mb_services_locationkind as
select
    id,
    value,
    label
from
    services_locationkind;

alter table mb_services_locationkind add primary key (id);

-- Indexes
create index idx_mb_services_locationkind_value
on mb_services_locationkind (value);

create index idx_mb_services_locationkind_label
on mb_services_locationkind (label);
