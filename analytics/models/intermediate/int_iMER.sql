SELECT
    'orientation'                                                                       AS kind,
    CAST(orientation_id AS text)                                                        AS event_id,
    orientation_creation_date                                                           AS date,
    orientation_prescriber_id                                                           AS user_id,
    user_main_activity                                                                  AS user_kind,
    user_is_manager                                                                     AS is_manager,
    structure_typology,
    structure_department,
    COALESCE(orientation_di_service_id IS NOT NULL, FALSE)                              AS is_di_service,
    COALESCE(user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber,
    NULL                                                                                AS generates_orientation
FROM {{ ref('int_orientation_user_service') }}
UNION ALL
SELECT
    'mobilisation'                                                                        AS kind,
    m.event_id,
    m.event_date                                                                          AS date,
    m.user_id,
    m.event_user_kind                                                                     AS user_kind,
    m.event_is_manager                                                                    AS is_manager,
    struct_members.structure_typology,
    struct_members.structure_department,
    m.event_is_di                                                                         AS is_di_service,
    COALESCE(m.user_main_activity IN ('accompagnateur', 'accompagnateur_offreur'), FALSE) AS is_prescriber,
    o_m.generates_orientation
FROM {{ ref('int_mobilisationevent_user') }} AS m
LEFT JOIN
    {{ ref('int_structure_members') }} AS struct_members
    ON m.user_id = struct_members.user_id AND m.event_structure_id = CAST(struct_members.structure_id AS text)
LEFT JOIN {{ ref('int_mobilisation_to_orientation') }} AS o_m
    ON m.event_id = o_m.mobilisation_id
