
with source_data as (

    select 
        "abc" as id,
        "2022-06-30" as run_time,
        3 as arrow
    union all
    select 
        "abcd" as id,
        "2022-06-30" as run_time,
        4 as arrow
)

select *
from source_data


