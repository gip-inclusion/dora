-- Utilisateurs sans rattachements ni invitations
-- e-mail validé ou non

-- noqa: disable=LT05

drop table if exists q_orphan_users;

create table q_orphan_users as
select
    mu.id                               as "ID utilisateur",
    mu.email                            as "E-mail",
    mu.first_name                       as "Nom",
    mu.last_name                        as "Prénom",
    mu.is_valid                         as "E-mail validé",
    mu.date_joined                      as "Date de création",
    mu.last_login                       as "Dernière connexion",
    (
        case
            when mu.date_joined > now() - interval '24 months' then false
            when mu.last_login is null then true
            else mu.last_login < now() - interval '24 months'
        end
    )                                   as "Compte inactif",
    (select ic_id is not null)          as "Inscrit IC",
    (select date_joined < '2022-10-03') as "Créé avant MEP IC"
from mb_user as mu
where
    not mu.is_staff
    and mu.id not in (select user_id from structures_structuremember)
    and mu.id not in (select user_id from structures_structureputativemember)
    and mu.id not in (select "ID utilisateur" from q_users_before_ic)
order by mu.date_joined desc;

-- Indexes et PK

alter table public.q_orphan_users add constraint q_orphan_users_pk primary key ( -- noqa: LT05
    "ID utilisateur"
);

create index q_orphan_users_valide_idx
on q_orphan_users ("E-mail validé");

create index q_orphan_users_date_joined_idx
on q_orphan_users ("Date de création");

comment on table q_orphan_users is 'Liste des utilisateurs non rattachés à une structure et sans invitation';
