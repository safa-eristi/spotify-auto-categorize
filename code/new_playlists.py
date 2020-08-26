playlists = [
    {
       'name': 'Seventies',
       'rules': [
           {
                'rule_type': 'track_data', # or 'audio_features'
                'comparison': 'startswith',
                'field': 'track#album#release_date',
                'value': '197'
           }
       ]
    },
    {
       'name': 'Eighties',
       'rules': [
           {
                'rule_type': 'track_data',
                'comparison': 'startswith',
                'field': 'track#album#release_date',
                'value': '198'
           }
       ]
    },
    {
       'name': 'Nineties',
       'rules': [
           {
                'rule_type': 'track_data',
                'comparison': 'startswith',
                'field': 'track#album#release_date',
                'value': '199'
           }
       ]
    },
    {
       'name': 'Oldies',
       'rules': [
           {
                'rule_type': 'track_data',
                'comparison': 'startswith',
                'field': 'track#album#release_date',
                'value': '19'
           }
       ]
    },
      {
         'name': 'Major Tracks',
         'rules': [
             {
                  'rule_type': 'audio_features',
                  'comparison': 'equals',
                  'field': 'mode',
                  'value': 1
             }
         ]
      },
      {
         'name': 'Minor Tracks',
         'rules': [
             {
                  'rule_type': 'audio_features',
                  'comparison': 'equals',
                  'field': 'mode',
                  'value': 0
             }
         ]
      },
      {
         'name': 'Instrumental Tracks',
         'rules': [
             {
                  'rule_type': 'audio_features',
                  'comparison': 'greaterthan',
                  'field': 'instrumentalness',
                  'value': 0.5
             }
         ]
      },
      {
         'name': 'Acoustic Tracks',
         'rules': [
             {
                  'rule_type': 'audio_features',
                  'comparison': 'greaterthan',
                  'field': 'acousticness',
                  'value': 0.8
             }
         ]
      },
      {
         'name': 'High Tempo Tracks',
         'rules': [
             {
                  'rule_type': 'audio_features',
                  'comparison': 'greaterthan',
                  'field': 'tempo',
                  'value': 120
             },
             {
                   'rule_type': 'audio_features',
                   'comparison': 'greaterthan',
                   'field': 'energy',
                   'value': 0.7
              }
         ]
      }
]
    