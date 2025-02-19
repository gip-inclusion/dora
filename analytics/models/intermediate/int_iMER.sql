SELECT
    'orientation'                                                                       AS kind,
    orientation_creation_date                                                           AS date,
    orientation_prescriber_id                                                           AS user_id,
    COALESCE(orientation_di_service_id IS NOT NULL, FALSE)                              AS is_di_service,
    COALESCE(user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber,
    NULL                                                                                AS generates_orientation
FROM {{ ref('int_orientation_user_service') }}
UNION ALL
SELECT
    'mobilisation'                                                                      AS kind,
    event_date                                                                          AS date,
    m.user_id,
    event_is_di                                                                         AS is_di_service,
    COALESCE(user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber,
    COALESCE(o_m.delay IS NOT NULL, FALSE)                                              AS generates_orientation
FROM {{ ref('int_mobilisationevent_user') }} as m
LEFT JOIN {{ ref('int_orientations_following_mobilisation') }} as o_m
    ON o_m.mobilisation_id = m.event_id
