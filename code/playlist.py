# -*- coding: utf-8 -*-

import restapi
import logger

class Playlist:
    def __init__(self, playlist_item, is_simple=False):
        self.name = playlist_item.get('name')
        self.value = playlist_item.get('id')
        self.id = playlist_item.get('id')
        self.href = playlist_item.get('href')
        self.is_public = playlist_item.get('public')
        self.disabled = False
        self.tracks = {}

        if is_simple is False:
            self.expand()


    def __str__(self):
        return self.name


    def get(self, property_name, *args):
        return getattr(self, property_name, self.name)


    def expand(self):
        logger.log('expanding the playlist class {}'.format(self.name))
        get_playlist_tracks_response = restapi.get_playlist_tracks(self.value)
        for item in get_playlist_tracks_response.get('items'):
            if item.get('track') == None:
                continue

            if item.get('track', {}).get('id', None) is not None:
                self.tracks[item.get('track').get('id')] = {'track_data': item}
        
        while get_playlist_tracks_response.get('next') is not None:
            get_playlist_tracks_response = restapi.get_url(get_playlist_tracks_response.get('next'))
            for item in get_playlist_tracks_response.get('items'):
                if item.get('track') == None:
                    continue

                if item.get('track').get('id') is not None:
                    self.tracks[item.get('track').get('id')] = {'track_data': item}

        track_ids = []
        for track_id in self.tracks.keys():
            track_ids.append(track_id)
            if len(track_ids) == 100:
                get_playlist_tracks_response = restapi.get_audio_features(track_ids)
                for audio_feature in get_playlist_tracks_response.get('audio_features'):
                    self.tracks[audio_feature.get('id')]['audio_features'] = audio_feature
                track_ids = [] 

        if len(track_ids) > 0:
            get_playlist_tracks_response = restapi.get_audio_features(track_ids)
            for audio_feature in get_playlist_tracks_response.get('audio_features'):
                self.tracks[audio_feature.get('id')]['audio_features'] = audio_feature
