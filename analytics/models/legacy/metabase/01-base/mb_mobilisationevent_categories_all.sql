-- NOTE(vperron) : this model and the other one about mobilisation events
-- makes me think that there is a weird and probably unnecessary schema issue here,
-- tables are similar to the point they can be JOINED but one has an 'id' and the other a 'di_id',
-- meaning they could probably be in the same table...


-- utilisé une seule fois

WITH src_event_categories AS (
    SELECT * FROM {{ source('dora', 'stats_mobilisationevent_categories') }}
),

src_di_event_categories AS (
    SELECT * FROM {{ source('dora', 'stats_dimobilisationevent_categories') }}
),

event_categories AS (
    SELECT
        'dora-'
        || src.mobilisationevent_id
        AS mobilisationevent_id,
        src.servicecategory_id
    FROM src_event_categories AS src
),

di_event_categories AS (
    SELECT
        'di-'
        || src.dimobilisationevent_id
        AS mobilisationevent_id,
        src.servicecategory_id
    FROM src_di_event_categories AS src
),

final AS (
    SELECT * FROM event_categories
    UNION
    SELECT *
    FROM di_event_categories
)

SELECT * FROM final
