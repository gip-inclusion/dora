WITH user_service_views AS (
    SELECT *
    FROM {{ ref('int_serviceview_user_service') }}
    WHERE
        event_is_logged IS TRUE
        AND event_is_staff IS FALSE
        AND event_is_manager IS FALSE
        AND event_is_structure_member IS FALSE
        AND event_is_structure_admin IS FALSE
),

finance_service_labels AS (
    SELECT *
    FROM {{ ref('int_service_funding_labels') }}
    WHERE fundinglabel_label IS NOT NULL
)

SELECT
    user_service_views.event_id,
    user_service_views.event_date,
    user_service_views.service_id,
    user_service_views.service_name,
    user_service_views.service_status,
    user_service_views.structure_name,
    finance_service_labels.fundinglabel_name AS funding_label
FROM user_service_views
INNER JOIN finance_service_labels ON user_service_views.service_id = finance_service_labels.service_id
