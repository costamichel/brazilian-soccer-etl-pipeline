WITH mandantes AS (
    SELECT
        id_time_mandante AS id_time,
        1 AS jogos_disputados,
        CASE WHEN gols_mandante > gols_visitante THEN 1 ELSE 0 END AS vitorias,
        CASE WHEN gols_mandante = gols_visitante THEN 1 ELSE 0 END AS empates,
        CASE WHEN gols_mandante < gols_visitante THEN 1 ELSE 0 END AS derrotas,
        gols_mandante AS gols_feitos,
        gols_visitante AS gols_sofridos
    FROM {{ ref('stg_partidas') }}
    WHERE gols_mandante IS NOT NULL AND gols_visitante IS NOT NULL
),

visitantes AS (
    SELECT
        id_time_visitante AS id_time,
        1 AS jogos_disputados,
        CASE WHEN gols_visitante > gols_mandante THEN 1 ELSE 0 END AS vitorias,
        CASE WHEN gols_visitante = gols_mandante THEN 1 ELSE 0 END AS empates,
        CASE WHEN gols_visitante < gols_mandante THEN 1 ELSE 0 END AS derrotas,
        gols_visitante AS gols_feitos,
        gols_mandante AS gols_sofridos
    FROM {{ ref('stg_partidas') }}
    WHERE gols_mandante IS NOT NULL AND gols_visitante IS NOT NULL
),

-- Empilhando os dados de jogos em casa e fora
todos_os_jogos AS (
    SELECT * FROM mandantes
    UNION ALL
    SELECT * FROM visitantes
),

-- Criando uma tabela temporária apenas com as agregações matemáticas
classificacao_calculada AS (
    SELECT
        id_time,
        SUM(jogos_disputados) AS partidas_jogadas,
        SUM(vitorias) AS vitorias,
        SUM(empates) AS empates,
        SUM(derrotas) AS derrotas,
        SUM(gols_feitos) AS gols_pro,
        SUM(gols_sofridos) AS gols_contra,
        SUM(gols_feitos) - SUM(gols_sofridos) AS saldo_gols,
        (SUM(vitorias) * 3) + SUM(empates) AS pontos
    FROM todos_os_jogos
    GROUP BY id_time
)

-- Trazendo o nome do time para o resultado final
SELECT
    c.id_time,
    t.nome, 
    c.partidas_jogadas,
    c.pontos,
    c.vitorias,
    c.empates,
    c.derrotas,
    c.gols_pro,
    c.gols_contra,
    c.saldo_gols
FROM classificacao_calculada c
LEFT JOIN {{ ref('stg_times') }} t  
    ON c.id_time = t.id
ORDER BY c.pontos DESC, c.vitorias DESC, c.saldo_gols DESC