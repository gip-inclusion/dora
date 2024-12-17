WITH src AS (
    SELECT * FROM {{ source('dora', 'stats_serviceview') }}
),

src_di AS (
    SELECT * FROM {{ source('dora', 'stats_diserviceview') }}
),

service_view AS (

    SELECT
        'dora-' || src.id              AS id,
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
        src.service_source             AS source,
        src.is_orientable,
        FALSE                          AS is_di,
        CAST(src.service_id AS text)   AS service_id,
        CAST(src.structure_id AS text) AS structure_id,
        service.name                   AS service_name,
        structure.name                 AS structure_name
    FROM
        src
    LEFT JOIN {{ source('dora', 'services_service') }} AS service ON src.service_id = service.id
    LEFT JOIN {{ source('dora', 'structures_structure') }} AS structure ON src.structure_id = structure.id
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
        src.source,
        FALSE                        AS is_orientable,
        TRUE                         AS is_di,
        CAST(src.service_id AS text) AS service_id,
        src.structure_id,
        src.service_name,
        src.structure_name
    FROM
        src_di AS src
),

final AS (
    SELECT * FROM service_view
    UNION
    SELECT * FROM di_service_view
)

SELECT * FROM final
