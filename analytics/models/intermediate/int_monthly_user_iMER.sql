SELECT
    usr.id                                        AS user_id,
    usr.is_manager,
    usr.main_activity                             AS user_kind,
    structure_typology,
    structure_department,
    date_trunc('month', iMER.date) AS events_month,
    count(distinct iMER.event_id)        AS nb_iMER
FROM {{ source('dora', 'users_user') }} AS usr
LEFT JOIN
    {{ ref('int_iMER') }} AS iMER
    ON usr.id = iMER.user_id
GROUP BY
    usr.id,
    usr.is_manager,
    structure_typology,
    structure_department,
    date_trunc('month', iMER.date)

