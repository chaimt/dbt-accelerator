{{
    config(
        materialized=('incremental' if target.name == 'prod' else 'view'),
        unique_key='time_id'
    )
}}

with source_data as (
    select 
        id,
        run_time,
        avg(arrow) as arrow_avg, 
        {{ dbt_utils.surrogate_key(["id","run_time"]) }} as time_id
    FROM {{ ref('example_domain_stg__model_c') }}
    GROUP BY 
        id, 
        run_time

)

select *
from source_data
