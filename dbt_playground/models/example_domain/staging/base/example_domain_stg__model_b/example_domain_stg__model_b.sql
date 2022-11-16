with source_data as (

    select 
        "abc" as id_key,
        "2022-06-30" as ref_time,
        3 as lines
    union all
    select 
        "abcd" as id_key,
        "2022-06-31" as ref_time,
        4 as lines
)

select *
from source_data