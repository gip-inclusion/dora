-- Décompte des recherches effectuées par des utilisateurs connectés :
-- non-gestionnaire, 
-- non-membre de l'équipe, 
-- et non-offreur seulement. 

drop view if exists v_searches_for_user;

create or replace view v_searches_for_user as
select
    anonymous_user_hash,
    date_part('doy', date)   as jour,
    date_part('week', date)  as semaine,
    date_part('month', date) as mois,
    date_part('year', date)  as annee,
    count(*)                 as nb
from mb_stats_searchview
where
    user_kind != 'offreur'
    and not is_manager
    and not is_staff
    and is_logged
group by
    anonymous_user_hash,
    jour,
    semaine,
    mois,
    annee
order by annee asc, jour asc, nb desc;
