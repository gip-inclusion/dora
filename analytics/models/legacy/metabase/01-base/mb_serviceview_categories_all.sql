WITH src_serviceview_categories AS (
    SELECT * FROM {{ source('dora', 'serviceview_categories') }}
),

src_di_serviceview_categories AS (
    SELECT * FROM {{ source('dora', 'di_serviceview_categories') }}
),

serviceview_categories AS (
    SELECT
        'dora-'
        || src.serviceview_id
        AS serviceview_id,
        src.servicecategory_id
    FROM src_serviceview_categories AS src
),

di_serviceview_categories AS (
    SELECT
        'di-'
        || src.diserviceview_id
        AS serviceview_id,
        src.servicecategory_id
    FROM src_di_serviceview_categories AS src
),

final AS (
    SELECT * FROM serviceview_categories
    UNION
    SELECT *
    FROM di_serviceview_categories
)

SELECT * FROM final
