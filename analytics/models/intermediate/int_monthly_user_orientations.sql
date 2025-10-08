SELECT
    usr.id                                          AS user_id,
    usr.is_manager,
    usr.main_activity                               AS user_kind,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', orientations.creation_date) AS events_month,
    COUNT(DISTINCT orientations.id)                 AS nb_orientations
FROM {{ ref('stg_user') }} AS usr
LEFT JOIN
    {{ source('dora', 'orientations_orientation') }} AS orientations
    ON usr.id = orientations.prescriber_id
LEFT JOIN
    {{ ref('int_structure_members') }} AS struct_members
    ON usr.id = struct_members.user_id
GROUP BY
    usr.id,
    usr.is_manager,
    usr.main_activity,
    struct_members.structure_typology,
    struct_members.structure_department,
    DATE_TRUNC('month', orientations.creation_date)
