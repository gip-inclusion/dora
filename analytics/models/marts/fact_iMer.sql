WITH int_iMer AS (
    SELECT * FROM {{ ref('int_iMER') }}
)

SELECT
    KIND,
    EVENT_ID,
    DATE,
    USER_ID,
    GENERATES_ORIENTATION
FROM int_iMer
