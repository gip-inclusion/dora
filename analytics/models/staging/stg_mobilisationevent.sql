WITH src_events AS (
    SELECT * FROM {{ source('dora', 'stats_mobilisationevent') }}
),

src_di_events AS (
    SELECT * FROM {{ source('dora', 'stats_dimobilisationevent') }}
),

events AS (
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
        CAST(src.structure_id AS text) AS structure_id,
        src.user_id,
        FALSE                          AS is_di

    FROM src_events AS src

),

di_events AS (
    SELECT
        'di-' || src.id                AS id,
        src.path,
        src.date,
        src.anonymous_user_hash,
        src.is_logged,
        src.is_staff,
        src.is_manager,
        src.is_an_admin,
        FALSE
        AS is_structure_admin,
        FALSE
        AS is_structure_member,
        src.user_kind,
        src.structure_department,
        CAST(src.structure_id AS text) AS structure_id,
        src.user_id,
        TRUE                           AS is_di
    FROM src_di_events AS src
),


final AS (
    SELECT * FROM events
    UNION
    SELECT *
    FROM di_events
    WHERE date >= '2024-01-01'
)

SELECT * FROM final
