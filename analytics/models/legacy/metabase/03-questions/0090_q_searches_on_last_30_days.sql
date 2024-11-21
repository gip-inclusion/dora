-- Question(s) concernée(s):
--   • "Recherches sur les 30 derniers jours"

drop table if exists q_searches_on_last_30_days;

create table q_searches_on_last_30_days as (
    select
        "search".id          as "id",
        "search".path        as "path",
        "search".date        as "date",
        "search".num_results as "num_results",
        "search".department  as "department",
        ss.label             as "label"
    from stats_searchview as "search"
    left join
        stats_searchview_categories as category
        on "search".id = category.searchview_id
    left join
        services_servicecategory as thematique
        on category.servicecategory_id = thematique.id
    left join
        structures_structuremember as member
        on "search".user_id = member.user_id
    left join mb_structure as structure on member.structure_id = structure.id
    left join
        structures_structure_national_labels as ssnl
        on structure.id = ssnl.structure_id
    left join
        structures_structurenationallabel as ss
        on ssnl.structurenationallabel_id = ss.id
    where
        "search".date >= now() - INTERVAL '30 days'
        and "search".is_staff = false
        and "search".is_manager = false
);
