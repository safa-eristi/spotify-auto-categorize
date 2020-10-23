# -*- coding: utf-8 -*-

import logging
import requests
from urllib.parse import urlencode


import flask
from flask import current_app


logger = logging.getLogger('flaskapp.blueprints.oauth')
bp = flask.Blueprint('oauth', __name__)


@bp.route('/authorize', methods=['GET', 'POST'])
def authorize():
    params = {
        'client_id': current_app.config['CLIENT_ID'],
        'client_secret': current_app.config['CLIENT_SECRET'],
        'redirect_uri': current_app.config['CALLBACK_URL'],
        'response_type': 'code',
        'scope': 'playlist-modify-private playlist-modify-public user-library-modify playlist-read-private playlist-read-collaborative user-library-read'
    }
    print(current_app.config['CALLBACK_URL'])
    url_params = urlencode(params)

    redirect_url = '{url}?{params}'.format(url=current_app.config['AUTHORIZATION_URL'], params=url_params)

    return flask.redirect(redirect_url)


@bp.route('/callback', methods=['GET', 'POST'])
def callback():
    print(flask.request.get_data())
    print(flask.request.args.to_dict())

    authorization_code = flask.request.args.get('code')

    if authorization_code is None:
        print('unable to get "code" from callback')
        return flask.abort(400)

    print('code: {}'.format(authorization_code))

    headers = {
        'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = {
        'client_id': current_app.config['CLIENT_ID'],
        'client_secret': current_app.config['CLIENT_SECRET'],
        'redirect_uri': current_app.config['CALLBACK_URL'],
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'response_type': 'code',
    }

    r = requests.post(current_app.config['TOKEN_URL'], params=params, headers=headers)

    response = {
        'json': r.json(),
        'status_code':  r.status_code,
    }

    return flask.jsonify(response)
