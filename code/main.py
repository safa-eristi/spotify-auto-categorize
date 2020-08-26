# -*- coding: utf-8 -*-

import base64
import codecs
import csv
import json
import os
import re

from schema import Schema, And, Use, Optional, SchemaError
from PyInquirer import prompt
from pprint import pprint



import config.settings
import logger
import restapi
import playlist
import new_playlists

# used when processing rule triggers
COMPARISON_EQUAL = 'equals'
COMPARISON_NOTEQUAL = 'notequals'
COMPARISON_STARTSWITH = 'startswith'
COMPARISON_ENDSWITH = 'endswith'
COMPARISON_CONTAINS = 'contains'
COMPARISON_GREATER_THAN = 'greaterthan'
COMPARISON_LESS_THAN = 'lessthan'
COMPARISON_IN = 'in'

RULE_TYPE_TRACK_DATA = 'track_data'
RULE_TYPE_AUDIO_FEATURES = 'audio_features'

TEMP_PLAYLIST_NAME = 'Temp For Script'

PLAYLIST_SCHEMA = Schema({
    'name': And(Use(str)),
    'rules': [{
        'rule_type': And(Use(str), lambda n: n == RULE_TYPE_TRACK_DATA or n == RULE_TYPE_AUDIO_FEATURES),
        'comparison': And(Use(str)),
        'field': And(Use(str)),
        'value': And(Use(str)),
    }]
})

current_user = None
temp_playlist = None

def validate_new_playlists():
    playlists = new_playlists.playlists

    for playlist in playlists:
        structure_ok = check_structure(playlist)
        logger.log('structure analysis result for playlist: {} is {}'.format(playlist.get('name'), structure_ok))

        if not structure_ok:
            return False

    return True


def check_structure(structure):
    try:
        PLAYLIST_SCHEMA.validate(structure)
        return True
    except SchemaError as e:
        logger.log('structure check failed with error {}'.format(e))
        return False


def execute_new_playlists(source_playlist_tracks, user_playlists):
    for new_playlist in new_playlists.playlists:
        execute_playlist(new_playlist, source_playlist_tracks, user_playlists)


def create_playlist(name):
    global current_user
    playlist = {
        'name': name,
        'public': False,
        'collaborative': False,
        'description': '{} playlist created automatically by this script: https://github.com/safa-eristi/spotify-auto-categorize'.format(name)
    }   
    logger.log('creating playlist {}'.format(name))

    return restapi.create_playlist(current_user.get('id'), playlist)


def execute_playlist(new_playlist, source_playlist_tracks, user_playlists):
    global current_user
    playlist_object = None
    track_list = []

    new_playlist_name = new_playlist.get('name')
    logger.log('executing playlist {}'.format(new_playlist_name))

    playlist_id = None
    for user_playlist in user_playlists:
        if new_playlist_name.lower() == user_playlist.name.lower():
            logger.log('playlist with name {} already exists, updating..'.format(new_playlist_name))
            playlist_id = user_playlist.id
            user_playlist.expand()
            playlist_object = user_playlist
            break

    if playlist_id is None:
        create_playlist_response = create_playlist(new_playlist.get('name'))
        if create_playlist_response is None:
            logger.log('playlist {} could not be created, please check the logs')
            return False

        logger.log('playlist {} is created successfuly'.format(new_playlist.get('name')))
        playlist_id = create_playlist_response.get('id')


    ## Execute the rules
    for track_id in source_playlist_tracks.keys():  
        rule_execution_result = apply_rules(source_playlist_tracks[track_id], new_playlist.get('rules'))
        if rule_execution_result is True:
            if playlist_object is not None:
                if track_id not in user_playlist.tracks.keys():
                    track_list.append(track_id)
            else:
                track_list.append(track_id)

    logger.log('{} songs will be added to the playlist {}'.format(len(track_list), new_playlist.get('name')))

    track_ids = []
    for track_id in track_list:
        track_ids.append(track_id)
        if len(track_ids) == 100:
            restapi.add_tracks_to_playlist(playlist_id, track_ids)
            track_ids = []

    if len(track_ids) > 0:
        restapi.add_tracks_to_playlist(playlist_id, track_ids)


def apply_rules(track, rules):
    for rule in rules:
        if rule.get('rule_type') == RULE_TYPE_AUDIO_FEATURES:
            item = track.get('audio_features')
        elif rule.get('rule_type') == RULE_TYPE_TRACK_DATA:
            item = track.get('track_data')
        else:
            item = None
            logger.log('this should not have happened')

        item_fields = rule.get('field').split(config.settings.RULE_FIELD_SEPERATOR)

        field_value = item
        for item_field in item_fields:
            field_value = field_value.get(item_field)
        
        rule_execution_result = apply_rule(rule.get('comparison'), field_value, rule.get('value'))
        if rule_execution_result is False:
            return False
                
    return True


def apply_rule(comparison, field_value, value):
    #print('comparison {} -> field_value {} -> value {}'.format(comparison, field_value, value))
    if comparison == COMPARISON_EQUAL:
        return field_value == value

    if comparison == COMPARISON_NOTEQUAL:
        return field_value != value

    if comparison == COMPARISON_STARTSWITH:
        return field_value.startswith(value)

    if comparison == COMPARISON_ENDSWITH:
        return field_value.endswith(value)

    if comparison == COMPARISON_CONTAINS:
        return value in field_value

    if comparison == COMPARISON_IN:
        return field_value in value

    if comparison == COMPARISON_GREATER_THAN:
        return field_value > value

    if comparison == COMPARISON_LESS_THAN:
        return field_value < value

    logger.log('unidentified rule.comparison: {}'.format(comparison))
    return False


def ask_preference():
    preference_prompt = {
        'type': 'list',
        'name': 'preference',
        'message': 'Do you want to choose a playlist to categorize or use your library',
        'choices': ['Choose Playlist', 'Use Library']
    }
    answers = prompt(preference_prompt)
    return answers['preference']


def get_source_playlist(user_playlists):
    global temp_playlist
    preference = ask_preference()

    if preference == 'Choose Playlist':
        questions = [
            {
                'type': 'list',
                'name': 'source_list_id',
                'message': 'Please select the source playlit to work with?',
                'choices': user_playlists
                
            }
        ]

        answer = prompt(questions)
        return answer.get('source_list_id')

    
    create_playlist_response = create_playlist(TEMP_PLAYLIST_NAME)
    playlist_id = create_playlist_response.get('id')
    temp_playlist = playlist_id

    all_track_ids = []
    all_tracks_response = restapi.get_all_tracks()
    for item in all_tracks_response.get('items'):
        if item.get('track') == None:
            continue

        if item.get('track', {}).get('id', None) is not None:
            all_track_ids.append(item.get('track', {}).get('id', None))
    
    while all_tracks_response.get('next') is not None:
        all_tracks_response = restapi.get_url(all_tracks_response.get('next'))
        for item in all_tracks_response.get('items'):
            if item.get('track') == None:
                continue

            if item.get('track', {}).get('id', None) is not None:
                all_track_ids.append(item.get('track', {}).get('id', None))

    track_ids = []
    for track_id in all_track_ids:
        track_ids.append(track_id)
        if len(track_ids) == 100:
            restapi.add_tracks_to_playlist(playlist_id, track_ids)
            track_ids = []

    if len(track_ids) > 0:
        restapi.add_tracks_to_playlist(playlist_id, track_ids)

    return playlist_id


def run():
    restapi.authenticate()

    # Check if new playlist have required keys and values
    if validate_new_playlists() is False:
        logger.log('at least one playlist have an error. please fix and run again')
        return

    # get current user
    global current_user
    current_user = restapi.get_user()

    # get user's playlists
    user_playlists = []
    get_playlists_response = restapi.get_playlists()
    for playlist_entry in get_playlists_response.get('items'):
        user_playlists.append(playlist.Playlist(playlist_entry, True))

    source_playlist_id = get_source_playlist(user_playlists)
    source_playlist = playlist.Playlist(restapi.get_playlist(source_playlist_id))

    execute_new_playlists(source_playlist.tracks, user_playlists)
    if temp_playlist is not None:
        logger.log('please remove the temporary playlist created by this script with name {}'.format(TEMP_PLAYLIST_NAME))


if __name__ == '__main__':
    logger.log('START')
    run()
    logger.log('END')




