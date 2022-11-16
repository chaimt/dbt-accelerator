{{ dbt_data_applications.aggregate_calendar_profile(
    sources=[
        {
            'source': ref('example_domain_stg__daily_model_a'), 
            'fields': ['points_sum'], 
            'foreign_key_mappings': {'app_key': 'store_id', 'a_time': 'ref_time'}
        },
        {
            'source': ref('example_domain_stg__daily_model_b'), 
            'fields': ['lines_count'], 
            'foreign_key_mappings': {'id_key': 'store_id'}
        },
        {
            'source': ref('example_domain_stg__daily_model_c'), 
            'fields': ['arrow_avg'], 
            'foreign_key_mappings': {'id': 'store_id', 'run_time': 'ref_time'}
        }
    ],
    keys=['store_id', 'ref_time'], 
    calendar={
        'add_calendar': True,
        'column_time_frame_key_name':"ref_time", 
        'calendar_name':"dim_calendar", 
        'date_field': 'date',
        'lower_calendar_limit':"2022-01-23"
        },
    custom_columns=[
        "CASE
          WHEN points_sum + arrow_avg > 10 THEN '10+'
          WHEN points_sum + arrow_avg >  5 THEN '6-10'
          WHEN points_sum + arrow_avg >  1 THEN '2-5'
          WHEN points_sum + arrow_avg =  1 THEN '1'
          ELSE '0'
        END AS smsbump_cs_tools_count"
    ]
) }} 
