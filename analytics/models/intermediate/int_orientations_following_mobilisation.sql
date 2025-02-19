-- use `distinct on` to deal with the case when more than one mobilisation preceed the orientation
SELECT DISTINCT ON (o.user_id, o.orientation_id)
    m.user_id,
    o.service_slug,
    m.event_id                                 AS mobilisation_id,
    o.orientation_id                           AS orientation_id,
    m.event_date                               AS mobilisation_date,
    o.orientation_creation_date                AS orientation_date,
    -- calculate delay between last mobilisation and orientation
    o.orientation_creation_date - m.event_date AS delay
FROM {{ ref('int_mobilisationevent_user') }} AS m 
LEFT JOIN {{ ref('int_orientation_user_service') }} AS o
-- orientations that follows mobilisations have the same user_id, are done in the hour after the mobilisation, and concern the same service (slug)
    ON m.user_id = o.user_id
    AND o.orientation_creation_date BETWEEN m.event_date AND m.event_date + INTERVAL '1 hour'
    AND SPLIT_PART(m.event_path, '/', 3) = o.service_slug
-- keep only orientations that follow mobilisations
WHERE (o.orientation_creation_date - m.event_date)::INTERVAL > INTERVAL '0 seconds'
ORDER BY o.user_id