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
),

views_per_service AS (
    SELECT
        service_id,
        service_name,
        service_status,
        structure_name,
        COUNT(DISTINCT event_id) AS number_of_views
    FROM user_service_views
    GROUP BY
        service_id,
        service_name,
        service_status,
        structure_name
)

SELECT
    views_per_service.service_id,
    views_per_service.service_name,
    views_per_service.service_status,
    views_per_service.structure_name,
    finance_service_labels.fundinglabel_name AS funding_label,
    views_per_service.number_of_views

FROM views_per_service
INNER JOIN finance_service_labels ON views_per_service.service_id = finance_service_labels.service_id
