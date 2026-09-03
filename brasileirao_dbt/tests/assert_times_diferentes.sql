-- tests/assert_times_diferentes.sql
select
    id_partida
from {{ ref('stg_partidas') }}
where id_time_mandante = id_time_visitante