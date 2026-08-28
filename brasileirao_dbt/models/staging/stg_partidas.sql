WITH source_data AS (
    SELECT *
    FROM {{ source('supabase_prod', 'fato_partidas') }}
)

SELECT *
FROM source_data