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
    SELECT * FROM {{ ref("int_users_with_iMer") }}
),

structure_members AS (
    SELECT
        user_id,
        MIN(creation_date) AS first_date_as_structure_member
    FROM {{ source('dora', 'structures_structuremember') }}
    GROUP BY user_id

)

SELECT
    usr.*,
    usr_with_imer.user_id IS NOT NULL     AS user_with_imer,
    structure_members.first_date_as_structure_member,
    structure_members.user_id IS NOT NULL AS user_is_structure_member
FROM usr
LEFT JOIN usr_with_imer
    ON usr.id = usr_with_imer.user_id
LEFT JOIN structure_members
    ON usr.id = structure_members.user_id
