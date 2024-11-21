-- Utilisateurs en attente de rattachement
-- (extension des données de `structures_structureputativemember`)

-- noqa: disable=LT05

drop table if exists mb_putative_members cascade;

create table mb_putative_members as
select
    mu.id               as "ID utilisateur",
    mu.first_name       as "Nom",
    mu.last_name        as "Prénom",
    mu.email            as "E-mail",
    mu.is_valid         as "E-mail validé",
    mu.date_joined      as "Date de création",
    mu.last_login       as "Dernière connexion",
    ms.name             as "Nom de la structure",
    ms.slug             as "SLUG",
    ms.dora_url         as "URL Dora",
    ms.department       as "Département",
    ss.creation_date    as "Date d'invitation",
    ss.is_admin         as "Invitation en tant qu'admin",
    -- invité : l'utilisateur ne s'est pas rattaché lui-même à la structure 
    ss.invited_by_admin as "Invitation par un admin",
    (
        case
            when mu.date_joined > now() - interval '24 months' then false
            when mu.last_login is null then true
            else mu.last_login < now() - interval '24 months'
        end
    )                   as "Compte inactif",
    -- TODO: un refactor avec une table utilitaire pour éviter les jointures ?
    (
        select count(*)
        from structures_structuremember as ssm
        inner join mb_user as mu2 on ssm.user_id = mu2.id and mu2.is_valid
        where ssm.is_admin and ssm.structure_id = ms.id
    )                   as "Nombre d'admins dans la structure",
    (
        ss.is_admin
        and (
            select count(*) = 0 from
                structures_structuremember as ssm
            inner join mb_user as mu2 on ssm.user_id = mu2.id and mu2.is_valid
            where
                ssm.structure_id = ss.structure_id
                and ssm.is_admin
        )
    )                   as "Premier admin de la structure",
    (
        select count(*)
        from structures_structuremember as ss2
        where
            ss2.user_id = mu.id
    )                   as "Membre d'autres structures"
from mb_user as mu
inner join structures_structureputativemember as ss on mu.id = ss.user_id
left join mb_structure as ms on ss.structure_id = ms.id
where
    not mu.is_staff
order by mu.date_joined desc;

-- Indexes 
create index mb_putative_members_date_joined_idx on mb_putative_members ("Date de création");
create index mb_putative_members_dpt_idx on mb_putative_members ("Département");
create index mb_putative_members_dpt_is_valid on mb_putative_members ("E-mail validé");

comment on table mb_putative_members is 'Liste des membres en attente de rattachement';
