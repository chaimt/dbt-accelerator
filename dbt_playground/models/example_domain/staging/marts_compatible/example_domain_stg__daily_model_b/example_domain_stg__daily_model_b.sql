{{
    config(
        materialized=('incremental' if target.name == 'prod' else 'view'),
        unique_key='time_id'
    )
}}

with source_data as (
    select 
        id_key,
        ref_time,
        sum(lines) as lines_count, 
        {{ dbt_utils.surrogate_key(["id_key","ref_time"]) }} as time_id
    FROM {{ ref('example_domain_stg__model_b') }}
    GROUP BY 
        id_key, 
        ref_time

)

select *
from source_data
