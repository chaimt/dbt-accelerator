{{ dbt_data_applications.profile(
    sources=[
        {   
            'source': ref('example_domain_stg__model_a'), 
            'fields': ['points'],
            'foreign_key_mappings': {'app_key': 'userId'}
        },
        {   
            'source': ref('example_domain_stg__model_b'), 
            'fields': ['lines'], 
            'foreign_key_mappings': {'id_key': 'userId'}
        },
        {   
            'source': ref('example_domain_stg__model_c'), 
            'fields': ['arrow'], 
            'foreign_key_mappings': {'id': 'userId'}
        }
    ],
    keys=['userId'], 
    custom_columns=[
        "CASE
          WHEN points + lines + arrow > 10 THEN '10+'
          WHEN points + lines + arrow >  5 THEN '6-10'
          WHEN points + lines + arrow >  1 THEN '2-5'
          WHEN points + lines + arrow =  1 THEN '1'
          ELSE '0'
        END AS smsbump_cs_tools_count"
    ]
) }} 
