SELECT
    usr.id                                        AS user_id,
    usr.is_manager,
    usr.main_activity                             AS user_kind,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', mobilisations.event_date) AS events_month,
    COUNT(DISTINCT mobilisations.event_id)        AS nb_mobilisations
FROM {{ ref('stg_user') }} AS usr
LEFT JOIN
    {{ ref('int_mobilisationevent_user') }} AS mobilisations
    ON usr.id = mobilisations.user_id
LEFT JOIN
    {{ ref('int_structure_members') }} AS struct_members
    ON usr.id = struct_members.user_id
GROUP BY
    usr.id,
    usr.main_activity,
    usr.is_manager,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', mobilisations.event_date)
