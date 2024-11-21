drop table if exists mb_service_suggestion;

create table mb_service_suggestion as
select service_suggestions_servicesuggestion.* -- noqa: AM04
from service_suggestions_servicesuggestion;

alter table mb_service_suggestion add primary key (id);
