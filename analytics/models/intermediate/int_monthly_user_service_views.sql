SELECT
    usr.id                                  AS user_id,
    usr.is_manager,
    usr.main_activity                       AS user_kind,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', service_views.date) AS events_month,
    COUNT(DISTINCT service_views.id)        AS nb_service_views
FROM {{ ref('stg_user') }} AS usr
LEFT JOIN
    {{ ref('stg_serviceview') }} AS service_views
    ON usr.id = service_views.user_id
LEFT JOIN
    {{ ref('int_structure_members') }} AS struct_members
    ON usr.id = struct_members.user_id
GROUP BY
    usr.id,
    usr.is_manager,
    usr.main_activity,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', service_views.date)
