drop view if exists mb_service;

create view mb_service as
select -- noqa: AM04
    *,
    (
        select concat('https://dora.inclusion.beta.gouv.fr/services/', slug)
    ) as dora_url
from mb_all_service where is_model is false;
