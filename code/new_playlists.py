playlists = [
    # {
    #    'name': 'Seventies',
    #    'playlist_id': None,
    #    'rules': [
    #        {
    #             'rule_type': 'track_data', # or 'audio_features'
    #             'comparison': 'startswith',
    #             'field': 'album#release_date',
    #             'value': '197'
    #        }
    #    ]
    # },
    # {
    #    'name': 'Eighties',
    #    'playlist_id': None,
    #    'rules': [
    #        {
    #             'rule_type': 'track_data',
    #             'comparison': 'startswith',
    #             'field': 'album#release_date',
    #             'value': '198'
    #        }
    #    ]
    # },
    # {
    #    'name': 'Nineties',
    #    'playlist_id': None,
    #    'rules': [
    #        {
    #             'rule_type': 'track_data',
    #             'comparison': 'startswith',
    #             'field': 'album#release_date',
    #             'value': '199'
    #        }
    #    ]
    # },
    # {
    #    'name': 'Oldies',
    #    'playlist_id': None,
    #    'rules': [
    #        {
    #             'rule_type': 'track_data',
    #             'comparison': 'startswith',
    #             'field': 'album#release_date',
    #             'value': '19'
    #        }
    #    ]
    # },
    {
       'name': 'Major Tracks',
       'playlist_id': None,
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
       'playlist_id': None,
       'rules': [
           {
                'rule_type': 'audio_features',
                'comparison': 'equals',
                'field': 'mode',
                'value': 0
           }
       ]
    }
]