# -*- coding: utf-8 -*-

import pprint
import time
from urllib.parse import urlencode

import flask
import requests

import config.settings


app = flask.Flask(__name__)
app.config['DEBUG'] = True


@app.route('/authorize', methods=['GET', 'POST'])
def authorize():
    params = {
        'client_id': config.settings.CLIENT_ID,
        'client_secret': config.settings.CLIENT_SECRET,
        'redirect_uri': config.settings.CALLBACK_URL,
        'response_type': 'code',
        'scope': 'playlist-modify-private playlist-modify-public user-library-modify playlist-read-private playlist-read-collaborative user-library-read'
    }

    url_params = urlencode(params)

    redirect_url = '{url}?{params}'.format(url=config.settings.AUTHORIZATION_URL, params=url_params)

    return flask.redirect(redirect_url)


@app.route('/oauth_callback', methods=['GET', 'POST'])
def oauth_callback():
    print(flask.request.get_data())
    print(flask.request.args.to_dict())

    authorization_code = flask.request.args.get('code')

    if authorization_code is None:
        print(u'unable to get "code" from callback')
        return flask.abort(400)

    print(u'code: {}'.format(authorization_code))

    headers = {
        'Accept': 'application/json',
        # 'Content-Type': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
    }

    params = {
        'client_id': config.settings.CLIENT_ID,
        'client_secret': config.settings.CLIENT_SECRET,
        'redirect_uri': config.settings.CALLBACK_URL,
        'code': authorization_code,
        'grant_type': 'authorization_code',
        'response_type': 'code',
    }

    r = requests.post(config.settings.TOKEN_URL, params=params, headers=headers)

    response = {
        'json': r.json(),
        'status_code':  r.status_code,
    }

    return flask.jsonify(response)


if __name__ == '__main__':
    app.run(port=8002, debug=True, threaded=False)