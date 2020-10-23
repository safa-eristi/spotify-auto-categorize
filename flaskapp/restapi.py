# -*- coding: utf-8 -*-

import codecs
import datetime
import time

import requests

import config.settings
import decorators
import logger
import base64

access_token = None


def refresh_token():
    payload = {
        'grant_type': 'refresh_token',
        'refresh_token': config.settings.REFRESH_TOKEN
    }

    auth_str = bytes('{}:{}'.format(config.settings.CLIENT_ID, config.settings.CLIENT_SECRET), 'utf-8')
    b64_auth_str = base64.b64encode(auth_str).decode('utf-8')
    headers = {'Authorization': 'Basic {encoded}'.format(encoded=b64_auth_str)}

    return requests.post('{host}/api/token'.format(host=config.settings.INSTANCE_URL), data=payload, headers=headers).json()


def authenticate(force=False):
    logger.log('Spotify API authentication')
    global access_token

    response = refresh_token()
    logger.log('Spotify API refresh token successful')

    access_token = response.get('access_token')
    logger.log('Spotify API authentication done')

    return True


def make_request(method, url, **kwargs):
    global access_token

    kwargs.update({
        'timeout': (30, 60),
    })

    if 'headers' not in kwargs:
        kwargs.update({
            'headers': {}
        })

    kwargs['headers'].update({
        'Authorization': 'Bearer {}'.format(access_token)
    })

    r = None

    try:
        r = requests.request(method, url, **kwargs)
    except Exception as exc:
        logger.log('Spotify REST API request error: [{method}] {url} => {exc}'.format(method=method, url=url, exc=exc))
        return make_request(method, url, **kwargs)

    if requests.codes.ok <= r.status_code < requests.codes.multiple_choices:
        logger.log('Spotify REST API request success: [{method}] {url} => HTTP {status_code}'.format(method=method, url=url, status_code=r.status_code))

    elif r.status_code == requests.codes.unauthorized:
        authenticate(force=True)
        return make_request(method, url, **kwargs)

    elif r.status_code == requests.codes.too_many_requests:
        logger.log('Spotify REST API request limit: [{method}] {url} => HTTP {status_code}'.format(method=method, url=url, status_code=r.status_code))

        rate_limit_limit = int(r.headers['X-RateLimit-Limit'])
        rate_limit_remaining = int(r.headers['X-RateLimit-Remaining'])
        rate_limit_reset = int(r.headers['X-RateLimit-Reset'])

        now = int(datetime.datetime.now().strftime('%s'))
        diff = rate_limit_reset - now

        logger.log('Spotify REST API X-RateLimit-Limit : {limit} || X-RateLimit-Remaining: {remaining} || X-RateLimit-Reset : {reset} || X-RateLimit-Sleep : {diff}'.format(limit=rate_limit_limit, remaining=rate_limit_remaining, reset=rate_limit_reset, diff=diff))

        time.sleep(diff)

        return make_request(method, url, **kwargs)

    else:
        logger.log('Spotify REST API request failure: [{method}] {url} => HTTP {status_code}'.format(method=method, url=url, status_code=r.status_code))

    return r


def make_api_request(method, endpoint, **kwargs):
    url = '{host}/{endpoint}'.format(host=config.settings.API_URL, endpoint=endpoint)

    return make_request(method, url, **kwargs)


def make_rest_request(method, resource, **kwargs):
    endpoint = 'v{version}/{resource}'.format(version=config.settings.API_VERSION, resource=resource)

    return make_api_request(method, endpoint, **kwargs)


@decorators.json_or_default(default=None)
def get_url(url):
    return make_request('GET', url)


@decorators.json_or_default(default=None)
def get_user():
    return make_rest_request('GET', 'me')


@decorators.json_or_default(default=None)
def get_playlists():
    return make_rest_request('GET', 'me/playlists', params={'limit': 50})


@decorators.json_or_default(default=None)
def get_playlist(playlist_id):
    return make_rest_request('GET', 'playlists/{}'.format(playlist_id))


@decorators.json_or_default(default=None)
def get_playlist_tracks(playlist_id):
    return make_rest_request('GET', 'playlists/{}/tracks'.format(playlist_id))


@decorators.json_or_default(default=None)
def get_audio_features(track_ids):
    return make_rest_request('GET', 'audio-features', params={'ids': ','.join(track_ids)})


@decorators.json_or_default(default=None)
def create_playlist(user_id, payload):
    return make_rest_request('POST', 'users/{user_id}/playlists'.format(user_id=user_id), json=payload)


@decorators.json_or_default(default=None)
def add_tracks_to_playlist(playlist_id, song_list):
    payload = {
        'uris': ['spotify:track:{}'.format(song_id) for song_id in song_list]
    }

    return make_rest_request('POST', 'playlists/{playlist_id}/tracks'.format(playlist_id=playlist_id), json=payload)


@decorators.json_or_default(default=None)
def get_all_tracks():
    return make_rest_request('GET', 'me/tracks', params={'limit': 50})
