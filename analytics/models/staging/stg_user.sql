WITH src AS (
    SELECT *
    FROM {{ source('dora', 'users_user') }}
    WHERE
        is_active IS TRUE
        AND is_valid IS TRUE
        AND is_staff IS FALSE
),

final AS (
    SELECT
        id,
        email,
        last_name,
        first_name,
        is_manager,
        departments,
        date_joined,
        last_login,
        last_service_reminder_email_sent,
        newsletter,
        main_activity,
        departments[1]                          AS department,
        last_service_reminder_email_sent        AS last_notification_email_sent,
        last_login IS NOT NULL                  AS is_activated
    FROM src
)

SELECT *
FROM final
