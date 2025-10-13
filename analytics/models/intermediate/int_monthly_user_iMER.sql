SELECT
    usr.id                         AS user_id,
    usr.is_manager,
    usr.main_activity              AS user_kind,
    structure_typology,
    structure_department,
    DATE_TRUNC('month', imer.date) AS events_month,
    COUNT(DISTINCT imer.event_id)  AS nb_imer
FROM {{ source('dora', 'users_user') }} AS usr
LEFT JOIN
    {{ ref('int_iMER') }} AS imer
    ON usr.id = imer.user_id
GROUP BY
    usr.id,
    usr.is_manager,
    structure_typology,
    structure_department,
    DATE_TRUNC('month', imer.date)
