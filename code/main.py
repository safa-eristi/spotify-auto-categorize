# -*- coding: utf-8 -*-

import base64
import codecs
import csv
import json
import os
import re

import config.settings
import logger
import restapi
import new_playlists

SOURCE_LIST_NAME = 'Liked'

# used when processing rule triggers
COMPARISON_EQUAL = 'equal'
COMPARISON_NOTEQUAL = 'notequal'
COMPARISON_STARTSWITH = 'startswith'
COMPARISON_ENDSWITH = 'endswith'
COMPARISON_CONTAINS = 'contains'
COMPARISON_IN = 'in'

PLAYLIST_MANDATORY_KEYS = ['name', 'playlist_id', 'tracks', 'rules']

current_user = None


def main():
    logger.log('Start')
    global current_user
    source_list = None

    restapi.authenticate()

    current_user = restapi.get_user()
    users_playlists = restapi.get_playlists()
    for item in users_playlists['items']:
        if item['name'] in [playlist.get('name') for playlist in new_playlists.playlists]:
            print('playlist with name: {} already exists, please remove it and run the script again'.format(item['name']))
            return 

    for item in users_playlists['items']:
        if item['name'] == SOURCE_LIST_NAME:
            source_list = item
            logger.log('found the source playlist: {}'.format(SOURCE_LIST_NAME))
            break

    if source_list is None:
        logger.log('could not find the source playlist with name {} in playlists'.format(SOURCE_LIST_NAME))
        return

    playlist_tracks = []
    playlist_response = restapi.get_playlist_tracks(source_list['id'])
    playlist_tracks.extend(playlist_response['items'])

    while playlist_response.get('next') is not None:
        playlist_response = restapi.get_url(playlist_response.get('next'))
        playlist_tracks.extend(playlist_response['items'])


    process_new_playlists(playlist_tracks)


def process_new_playlists(playlist_tracks):
    for new_playlist in new_playlists.playlists:
        if is_playlist_executable(new_playlist):
            execute_playlist(new_playlist, playlist_tracks)


def is_playlist_executable(new_playlist):
    keys_exist = True
    for key in PLAYLIST_MANDATORY_KEYS:
        if key not in new_playlist.keys():
            logger.log('playlist entry {} does not have the mandatory key "{}", thus is not applicable'.format(new_playlist, key))
            keys_exist = False
            break

    if not keys_exist or not are_rules_applicable(new_playlist.get('rules')):
        return False

    return True


def are_rules_applicable(rules):
    for rule in rules:
        if is_rule_applicable(rule) is False:
            return False
    return True


def execute_playlist(new_playlist, playlist_tracks):
    global current_user
    logger.log('executing playlist {}'.format(new_playlist.get('name')))

    playlist = {
        'name': new_playlist.get('name'),
        'public': False,
        'collaborative': False,
        'description': '{} playlist'.format(new_playlist.get('name'))
    }   
    logger.log('creating playlist {}'.format(new_playlist.get('name')))

    response = restapi.create_playlist(current_user.get('id'), playlist)
    if response is None:
        logger.log('playlist {} could not be created, please check the logs')
        return False

    logger.log('playlist {} is created successfuly'.format(new_playlist.get('name')))
    new_playlist['playlist_id'] = response.get('id')


    ## Execute the rules
    #for track in playlist_tracks:
    #    for new_playlist in new_playlists.playlists:
    #        apply_rule()



def is_rule_applicable(rule):
    field = rule.get('field', None)
    comparison = rule.get('comparison', None)
    value = rule.get('value', None)

    if field is None:
        logger.log('rule {} must have the key "field"'.format(rule))
        return False


    if comparison is None:
        logger.log('rule {} must have the key "comparison"'.format(rule))
        return False


    if value is None:
        logger.log('rule {} must have the key "value"'.format(rule))
        return False

    if not isinstance(field, (str,)):
        logger.log('rule.field must be str: {}'.format(rule))
        return False

    if not isinstance(comparison, (str,)):
        logger.log('rule.comparison must be str: {}'.format(rule))
        return False

    #item_fields = rule['field'].split(config.settings.RULE_FIELD_SEPERATOR)
    #TODO add check for field existance
    return True


def apply_rule(comparison, value):
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

    logger.log('unidentified rule.comparison: {}'.format(comparison))
    return False

if __name__ == '__main__':
    main()




