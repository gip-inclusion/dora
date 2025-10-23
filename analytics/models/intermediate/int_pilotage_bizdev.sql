-- nombre de services publiés par structure
WITH structures_counts AS (
    SELECT
        structure_id,
        structure_department,
        SUM(CASE WHEN service_status = 'PUBLISHED' THEN 1 ELSE 0 END) AS nb_services_publies
    FROM
        {{ ref('int_service_structure') }}
    GROUP BY structure_id, structure_department
),

structures_act AS (
    SELECT
        sc.structure_department,
        MAX(si."Num Dea Brsa")                                                                                             AS num_dea_brsa,
        COUNT(DISTINCT sc.structure_id) FILTER (WHERE sc.nb_services_publies >= 1)                                         AS structures_actives,
        (COUNT(DISTINCT sc.structure_id) FILTER (WHERE sc.nb_services_publies >= 1))/(SQRT(MAX(si."Num Dea Brsa") / 1000)) AS maturite
    FROM structures_counts AS sc
    LEFT JOIN {{ ref('stats_insertion') }} AS si
        ON si."Code Dept" = sc.structure_department
    GROUP BY sc.structure_department
),

structures_acc AS (
    SELECT
        structure_department,
        COUNT(DISTINCT user_id) AS "Nombre d'accompagnateurs inscrits"
    FROM
        {{ ref('int_structure_members') }}
    WHERE user_main_activity IN ('accompagnateur', 'accompagnateur_offreur')
    GROUP BY structure_department
)

SELECT
    sc.structure_department                                            AS "Département",
    MAX(sact.structures_actives)                                       AS "Nombre de structures activées",
    MAX(sact.num_dea_brsa)                                             AS "Nombre de DEA et BRSA",
    MAX(sact.maturite)                                                 AS "Maturité",
    CASE
        WHEN MAX(sact.maturite) >= 15 THEN 4
        WHEN MAX(sact.maturite) >= 8 THEN 3
        WHEN MAX(sact.maturite) >= 5 THEN 2
        ELSE 1
    END                                                                AS "Score maturité",
    SUM(CASE WHEN serv.service_status = 'PUBLISHED' THEN 1 ELSE 0 END) AS "Nombre de services publiés",
    MAX(sacc."Nombre d'accompagnateurs inscrits")                      AS "Nombre d'accompagnateurs inscrits"
FROM
    structures_counts AS sc
LEFT JOIN structures_acc AS sacc
    ON sacc.structure_department = sc.structure_department
LEFT JOIN structures_act AS sact
    ON sact.structure_department = sc.structure_department
LEFT JOIN {{ ref('int_service_structure') }} AS serv
    ON serv.structure_id = sc.structure_id
GROUP BY
    sc.structure_department
ORDER BY
    sc.structure_department
