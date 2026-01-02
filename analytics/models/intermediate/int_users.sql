-- Je change ici la materialisation car je ne peux pas changer 
-- drastiquement la materialisation des tables intermediate
-- que par defaut je prefère être view
{{ config(
    materialized='view'
) }}


WITH usr AS (
    SELECT * FROM {{ ref('stg_user') }}
),

usr_with_imer AS (
    SELECT * FROM {{ ref("eph_users_with_iMer") }}
)

SELECT
    usr.*,
    usr_with_imer.user_id IS NOT NULL       AS user_with_imer
FROM usr
LEFT JOIN usr_with_imer
    ON usr.id = usr_with_imer.user_id
