WITH src AS (
    SELECT * FROM {{ source('dora', 'users_user') }}
    WHERE is_active IS TRUE
),

final AS (
    SELECT
        id,
        ic_id,
        email,
        last_name,
        first_name,
        is_valid,
        is_staff,
        is_manager,
        departments,
        date_joined,
        last_login,
        last_service_reminder_email_sent,
        newsletter,
        main_activity,
        departments[1]                   AS department,
        last_service_reminder_email_sent AS last_notification_email_sent
    FROM src
)

SELECT * FROM final
