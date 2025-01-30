SELECT
    {{ dbt_utils.star(relation_alias='struct_member', from=ref('int_structure_member')) }},
    struct_labels.national_label_name
FROM {{ ref('int_structure_member') }} AS struct_member
LEFT JOIN {{ ref('int_structure_labels') }} AS struct_labels
    ON struct_member.structure_id = struct_labels.structure_id
WHERE struct_member.user_main_activity IN ('accompagnateur', 'accompagnateur_offreur')