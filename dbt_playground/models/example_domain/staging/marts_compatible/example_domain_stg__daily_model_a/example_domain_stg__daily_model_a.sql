{{
    config(
        materialized=('incremental' if target.name == 'prod' else 'view'),
        file_format='delta',
        unique_key='time_id',
        incremental_strategy = 'merge',
    )
}}

with source_data as (
    select 
        app_key,
        a_time,
        sum(points) as points_sum, 
        {{ dbt_utils.surrogate_key(["app_key","a_time"]) }} as time_id
    FROM {{ ref('example_domain_stg__model_a') }}
    GROUP BY 
        app_key, 
        a_time

)

select *
from source_data


