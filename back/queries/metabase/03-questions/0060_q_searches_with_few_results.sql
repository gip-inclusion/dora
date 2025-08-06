-- Question(s) concernée(s):
--   • "Nombre de recherches aboutissant à peu de résultats (<6)"
--   • "Nombre de recherches aboutissant à 0 résultat" 

drop table if exists q_searches_with_few_results;

create table q_searches_with_few_results as (
    select
        "search".id          as "id",
        "search".path        as "path",
        "search".date        as "date",
        "search".num_results as "num_results",
        "search".department  as "department",
        ss.label             as "label",
        category.label       as "category"
    from stats_searchview as "search"
    left join
        stats_searchview_categories as "service"
        on "search".id = "service".searchview_id
    left join
        services_servicecategory as category
        on "service".servicecategory_id = category.id
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
        "search".num_results < 6
        and "search".is_staff = false
        and "search".is_manager = false
);
