
with source_data as (

    select 
        "abc" as app_key,
        "2022-06-30" as a_time,
        3 as points
    union all
    select 
        "abcd" as app_key,
        "2022-06-30" as a_time,
        4 as points
)

select *
from source_data


