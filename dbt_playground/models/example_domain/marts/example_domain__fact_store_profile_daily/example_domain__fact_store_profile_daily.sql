{{ dbt_data_applications.aggregate_daily_profile(
    sources=[
        {
            'source': ref('example_domain_stg__daily_model_a'), 
            'fields': ['points_sum'],
            'foreign_key_mappings': {'a_time': 'ref_time'}
        },
        {
            'source': ref('example_domain_stg__daily_model_b'), 
            'fields': ['lines_count'], 
            'foreign_key_mappings': {'id_key': 'app_key'}
        },
        {
            'source': ref('example_domain_stg__daily_model_c'), 
            'fields': ['arrow_avg'], 
            'foreign_key_mappings': {'id': 'app_key', 'run_time': 'ref_time'}
        }
    ],
    keys=['app_key', 'ref_time'], 
    calendar={
        'add_calendar': True,
        'column_foreign_key_name': "app_key",
        'column_time_frame_key_name': "ref_time", 
        'lower_calendar_limit': "2022-06-30"
        }
) }}   
