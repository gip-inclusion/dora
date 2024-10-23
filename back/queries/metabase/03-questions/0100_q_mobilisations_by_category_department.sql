-- Question(s) concernée(s):
--   • "Nombre de mobilisations par thématique"

drop table if exists q_mobilisations_by_category_department;

create table q_mobilisations_by_category_department as (
    select
        mobilisation.id      as "id",
        mobilisation.path    as "path",
        mobilisation.date    as "date",
        structure.department as "department",
        ss.label             as "label",
        category.label       as "category"
    from stats_mobilisationevent as mobilisation
    left join
        services_service_categories as "service"
        on mobilisation.service_id = "service".service_id
    left join
        services_servicecategory as category
        on "service".servicecategory_id = category.id
    left join
        structures_structuremember as member
        on mobilisation.user_id = member.user_id
    left join mb_structure as structure on member.structure_id = structure.id
    left join
        structures_structure_national_labels as ssnl
        on structure.id = ssnl.structure_id
    left join
        structures_structurenationallabel as ss
        on ssnl.structurenationallabel_id = ss.id
    where
        mobilisation.is_staff = false
        and mobilisation.is_manager = false
        and mobilisation.is_structure_member = false
        and mobilisation.is_structure_admin = false
);
