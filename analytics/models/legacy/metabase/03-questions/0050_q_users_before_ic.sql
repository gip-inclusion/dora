-- Utilisateurs sans invitations n'ayant pas validé leur email 
-- avant la mise en production d'inclusion-connect
-- a.k.a utilisateurs à supprimer

-- noqa: disable=LT05

drop table if exists q_users_before_ic;

create table q_users_before_ic as
select
    mu.id                           as "ID utilisateur",
    mu.email                        as "E-mail",
    mu.date_joined                  as "Date de création",
    (
        case
            when mu.date_joined > now() - interval '24 months' then false
            when mu.last_login is null then true
            else mu.last_login < now() - interval '24 months'
        end
    )                               as "Compte inactif",
    (mu.date_joined < '2022-10-03') as "Créé avant IC"
from mb_user as mu
where
    not mu.is_staff
    -- adresse e-mail non validée :
    and not mu.is_valid
    -- aucun rattachement en attente : 
    and mu.id not in (select user_id from structures_structureputativemember where not invited_by_admin)
    -- aucune connexion IC :
    and mu.ic_id is null
order by mu.date_joined desc;

-- Indexes et PK

alter table public.q_users_before_ic add constraint q_users_before_ic_pk primary key ( -- noqa: LT05
    "ID utilisateur"
);

create index q_users_before_ic_date_joined_idx
on q_users_before_ic ("Date de création");

comment on table q_users_before_ic is 'Utilisateurs avec e-mail non validé, créés avant IC';
