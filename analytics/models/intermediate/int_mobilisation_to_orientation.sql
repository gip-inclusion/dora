{{ config(
    materialized='view'
) }}

SELECT DISTINCT ON (m.user_id, m.event_id)
    m.user_id,
    m.event_id                                 AS mobilisation_id,
    o.orientation_id                           AS first_following_orientation_id,
    m.event_date                               AS mobilisation_date,
    o.orientation_creation_date                AS first_following_orientation_date,
    o.orientation_creation_date - m.event_date AS delay,
    o.orientation_id IS NOT NULL               AS generates_orientation
FROM {{ ref('int_mobilisationevent_user') }} AS m
LEFT JOIN {{ ref('int_orientation_user_service') }} AS o
-- orientations that follows mobilisations have the same user_id, are done in the hour after the mobilisation, and concern the same service (slug)
    ON
        m.user_id = o.user_id
        AND o.orientation_creation_date BETWEEN m.event_date AND m.event_date + INTERVAL '1 hour'
        AND SPLIT_PART(m.event_path, '/', 3) = o.service_slug
ORDER BY
    m.user_id ASC,
    m.event_id ASC,
    o.orientation_creation_date ASC
