WITH partidas AS (
    -- A função ref() é o coração do dbt. Ela lê o modelo stg_partidas,
    -- independente de qual schema ou banco de dados ele esteja rodando.
    SELECT *
    FROM {{ ref('stg_partidas') }}
)

SELECT 
    *,
    -- Exemplo de coluna calculada: carimbando a data exata em que o dbt processou o dado
    CURRENT_DATE AS data_atualizacao_dbt
FROM partidas