SELECT
    acc.id                          AS id_prescriber,
    acc.email                       AS email_prescriber,
    acc.last_name                   AS last_name_prescriber,
    acc.first_name                  AS first_name_prescriber,
    acc.last_login                  AS last_login_prescriber,
    acc.main_activity               AS main_activity_prescriber,
    nb_orient.last_orientation_date,
    COALESCE(total_orientations, 0) AS total_orientations
FROM {{ ref('stg_accompagnateurs') }} AS acc
LEFT JOIN {{ ref('stg_nb_orientations_per_user') }} AS nb_orient
    ON acc.id = nb_orient.prescriber_id
WHERE
    nb_orient.total_orientations IS NULL
    OR nb_orient.total_orientations = 1
