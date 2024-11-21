WITH logs AS (
    SELECT * FROM {{ source('dora', 'action_logs') }}
    WHERE
        msg LIKE 'process_notification_tasks:%'
        -- log level 20 => INFO
        AND level = 20
),

final AS (
    SELECT
        created_at                              AS date_creation,
        CAST(payload ->> 'nbCandidates' AS int) AS nb_candidats,
        CAST(payload ->> 'nbProcessed' AS int)  AS nb_traitees,
        CAST(payload ->> 'nbObsolete' AS int)   AS nb_obsoletes,
        CAST(payload ->> 'nbErrors' AS int)     AS nb_erreurs,
        payload ->> 'taskType'                  AS tache
    FROM logs
)

SELECT * FROM final
