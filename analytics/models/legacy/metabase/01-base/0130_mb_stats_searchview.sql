drop table if exists mb_stats_searchview cascade;

create table mb_stats_searchview as
select
    "search".id,
    "search".path,
    "search".date,
    "search".anonymous_user_hash,
    "search".is_logged,
    "search".is_staff,
    "search".is_manager,
    "search".is_an_admin,
    "search".user_kind,
    "search".department,
    "search".city_code,
    "search".num_results,
    "search".user_id,
    "search".num_di_results,
    "search".num_di_results_top10,
    "search".results_slugs_top10
from stats_searchview as "search";

-- Keys & constraints
alter table mb_stats_searchview add primary key (id);

-- Indexes 
create index idx_mb_stats_searchview_is_staff_is_manager_is_logged
on mb_stats_searchview using btree (
    "is_staff", "is_manager", "is_logged"
);
create index idx_mb_stats_searchview_user_id
on mb_stats_searchview using btree (
    "user_id"
);
