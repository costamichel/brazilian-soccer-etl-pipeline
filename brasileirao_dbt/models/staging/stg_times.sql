WITH source_data AS (
    SELECT *
    FROM {{ source('supabase_prod', 'dim_times') }}
)

SELECT *
FROM source_data