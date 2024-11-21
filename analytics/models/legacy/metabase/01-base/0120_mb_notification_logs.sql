-- Historique des traitements de tâches de notification

-- noqa: disable=LT05

drop table if exists mb_notification_logs cascade;

create table mb_notification_logs as
select
    created_at                        as "date_creation",
    (payload ->> 'nbCandidates')::int as "nb_candidats",
    (payload ->> 'nbProcessed')::int  as "nb_traitees",
    (payload ->> 'nbObsolete')::int   as "nb_obsoletes",
    (payload ->> 'nbErrors')::int     as "nb_erreurs",
    payload ->> 'taskType'            as "tache"
from logs_actionlog
where
    msg like 'process_notification_tasks:%'
    -- log level 20 => INFO
    and level = 20;

-- Indexes
create index mb_notification_logs_date_creation_idx on mb_notification_logs ("date_creation");
create index mb_notification_logs_tache_idx on mb_notification_logs ("tache");

comment on table mb_notification_logs is 'Historique des tâches de traitement de notification';
