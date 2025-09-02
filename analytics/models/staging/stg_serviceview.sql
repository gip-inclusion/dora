WITH src AS (
    SELECT * FROM {{ source('dora', 'stats_serviceview') }}
),

src_di AS (
    SELECT * FROM {{ source('dora', 'stats_diserviceview') }}
),

service_view AS (

    SELECT
        'dora-' || src.id            AS id,
        src.path,
        src.date,
        src.anonymous_user_hash,
        src.is_logged,
        src.is_staff,
        src.is_manager,
        src.is_an_admin,
        src.is_structure_admin,
        src.is_structure_member,
        src.user_kind,
        src.structure_department,
        src.user_id,
        CAST(src.service_id AS TEXT) AS service_id,
        src.service_source           AS source,
        src.is_orientable,
        FALSE                        AS is_di
    FROM
        src
),

di_service_view AS (

    SELECT
        'di-' || src.id              AS id,
        src.path,
        src.date,
        src.anonymous_user_hash,
        src.is_logged,
        src.is_staff,
        src.is_manager,
        src.is_an_admin,
        FALSE                        AS is_structure_admin,
        FALSE                        AS is_structure_member,
        src.user_kind,
        src.structure_department,
        src.user_id,
        CAST(src.service_id AS TEXT) AS service_id,
        src.source,
        FALSE                        AS is_orientable,
        TRUE                         AS is_di
    FROM
        src_di AS src
),

final AS (
    SELECT * FROM service_view
    UNION
    SELECT * FROM di_service_view
    WHERE
        CAST(date AS DATE) >= '2024-01-01'
        AND is_staff IS FALSE
)

SELECT * FROM final
