SELECT
    'orientation'                                                                       AS kind,
    orientation_creation_date                                                           AS date,
    orientation_prescriber_id                                                           AS user_id,
    COALESCE(orientation_di_service_id IS NOT NULL, FALSE)                              AS is_di_service,
    COALESCE(user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber
FROM {{ ref('int_orientation_user_service') }}
UNION ALL
SELECT
    'mobilisation'                                                                      AS kind,
    event_date                                                                          AS date,
    user_id,
    event_is_di                                                                         AS is_di_service,
    COALESCE(user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber
FROM {{ ref('int_mobilisationevent_user') }}
