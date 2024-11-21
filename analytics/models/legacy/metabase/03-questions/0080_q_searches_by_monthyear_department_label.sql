-- Question(s) concernée(s):
--   • "Evolution du nombre de recherhces - avec typologie"

drop table if exists q_searches_by_monthyear_department_label;

create table q_searches_by_monthyear_department_label as (
    select
        "search".department               as "department",
        ss.label                          as "label",
        to_char("search".date, 'YYYY-MM') as "month_year",
        count(distinct "search".id)       as "count"
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
        "search".is_staff = false
        and "search".is_manager = false
    group by
        to_char("search".date, 'YYYY-MM'),
        "search".department,
        ss.label
);
