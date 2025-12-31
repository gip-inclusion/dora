SELECT user_id
FROM {{ ref('int_iMER') }}
GROUP BY user_id
