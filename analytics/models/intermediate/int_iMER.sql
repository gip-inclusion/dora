SELECT
    'orientation'             as kind,
    orientation_creation_date as date,
    orientation_prescriber_id as user_id,
    service_id,
    CASE 
        WHEN orientation_di_service_id IS NOT NULL THEN TRUE ELSE FALSE 
    END                       as is_di_service,
    CASE
        WHEN user_main_activity = 'accompagnateur' or user_main_activity = 'accompagnateur_offreur' THEN TRUE ELSE FALSE
    END                       as is_prescriber
FROM {{ ref('int_orientation_user_service') }}
UNION ALL
SELECT
    'mobilisation'            as kind,
    event_date                as date,
    user_id                   as user_id,
    event_is_di               as is_di_service,
    CASE
        WHEN user_main_activity = 'accompagnateur' or user_main_activity = 'accompagnateur_offreur' THEN TRUE ELSE FALSE
    END                       as is_prescriber
FROM {{ ref('int_mobilisationevent_user') }}
