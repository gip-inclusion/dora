SELECT *
FROM {{ ref('stg_user') }}
WHERE
    last_login IS NOT NULL
    AND main_activity IN ('accompagnateur', 'accompagnateur_offreur')
