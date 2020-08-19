# Spotify Rule Based Playlist Creator

Python script to extract songs from a Spotify playlist according to user-defined rules and put them in a new playlist

Rules can depend on either:
	

 - The track data itself (e.g. album release date)
 - The audio features of the track

https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/


## Audio Features

    {
	  "duration_ms" : 255349,
	  "key" : 5,
	  "mode" : 0,
	  "time_signature" : 4,
	  "acousticness" : 0.514,
	  "danceability" : 0.735,
	  "energy" : 0.578,
	  "instrumentalness" : 0.0902,
	  "liveness" : 0.159,
	  "loudness" : -11.840,
	  "speechiness" : 0.0461,
	  "valence" : 0.624,
	  "tempo" : 98.002,
	  "id" : "06AKEBrKUckW0KREUWRnvT",
	  "uri" : "spotify:track:06AKEBrKUckW0KREUWRnvT",
	  "track_href" : "https://api.spotify.com/v1/tracks/06AKEBrKUckW0KREUWRnvT",
	  "analysis_url" : "https://api.spotify.com/v1/audio-analysis/06AKEBrKUckW0KREUWRnvT",
	  "type" : "audio_features"
	}

## Track Data

```
{
  "album": {
    "album_type": "single",
    "artists": [
      {
        "external_urls": {
          "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
        },
        "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
        "id": "6sFIWsNpZYqfjUpaCgueju",
        "name": "Carly Rae Jepsen",
        "type": "artist",
        "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
      }
    ],
    "available_markets": [
      "AD",
      "AR"
    ],
    "external_urls": {
      "spotify": "https://open.spotify.com/album/0tGPJ0bkWOUmH7MEOR77qc"
    },
    "href": "https://api.spotify.com/v1/albums/0tGPJ0bkWOUmH7MEOR77qc",
    "id": "0tGPJ0bkWOUmH7MEOR77qc",
    "images": [
      {
        "height": 640,
        "url": "https://i.scdn.co/image/966ade7a8c43b72faa53822b74a899c675aaafee",
        "width": 640
      }
    ],
    "name": "Cut To The Feeling",
    "release_date": "2017-05-26",
    "release_date_precision": "day",
    "type": "album",
    "uri": "spotify:album:0tGPJ0bkWOUmH7MEOR77qc"
  },
  "artists": [
    {
      "external_urls": {
        "spotify": "https://open.spotify.com/artist/6sFIWsNpZYqfjUpaCgueju"
      },
      "href": "https://api.spotify.com/v1/artists/6sFIWsNpZYqfjUpaCgueju",
      "id": "6sFIWsNpZYqfjUpaCgueju",
      "name": "Carly Rae Jepsen",
      "type": "artist",
      "uri": "spotify:artist:6sFIWsNpZYqfjUpaCgueju"
    }
  ],
  "available_markets": [
    "AD",
    "AR",
  ],
  "disc_number": 1,
  "duration_ms": 207959,
  "explicit": false,
  "external_ids": {
    "isrc": "USUM71703861"
  },
  "external_urls": {
    "spotify": "https://open.spotify.com/track/11dFghVXANMlKmJXsNCbNl"
  },
  "href": "https://api.spotify.com/v1/tracks/11dFghVXANMlKmJXsNCbNl",
  "id": "11dFghVXANMlKmJXsNCbNl",
  "is_local": false,
  "name": "Cut To The Feeling",
  "popularity": 63,
  "preview_url": "https://p.scdn.co/mp3-preview/3eb16018c2a700240e9dfb8817b6f2d041f15eb1?cid=774b29d4f13844c495f206cafdad9c86",
  "track_number": 1,
  "type": "track",
  "uri": "spotify:track:11dFghVXANMlKmJXsNCbNl"
}
```


# Playlists Dictionary

New playlists should be in the **new_playlists.py** file.

    {
           'name': 'High Tempo Tracks',
           'playlist_id': None,
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

