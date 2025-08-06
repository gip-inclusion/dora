-- Décompte des vues de structure par utilisateur connecté : 
-- non-gestionnaire, 
-- non-membre de l'équipe, 
-- pas une structure dont l'utilisateur est membre,
-- et non-offreur seulement. 

drop view if exists v_structure_views_for_user;

create or replace view v_structure_views_for_user as
select
    anonymous_user_hash,
    date_part('doy', date)   as jour,
    date_part('week', date)  as semaine,
    date_part('month', date) as mois,
    date_part('year', date)  as annee,
    count(*)                 as nb
from stats_structureview as ss
where
    user_kind != 'offreur'
    and not is_manager
    and not is_staff
    and is_logged
    -- l'utilisateur ne visualise pas une structure dont il est membre
    and user_id not in (
        select ss2.user_id
        from structures_structuremember as ss2
        where ss2.structure_id = ss.structure_id
    )
group by
    anonymous_user_hash,
    jour,
    semaine,
    mois,
    annee
order by annee asc, jour asc, nb desc;
