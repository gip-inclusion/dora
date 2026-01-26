WITH int_imer AS (
    SELECT * FROM {{ ref('int_iMER') }}
)

SELECT
    kind,
    event_id,
    date,
    user_id,
    generates_orientation
FROM int_imer
