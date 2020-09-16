import logging
import requests
from urllib.parse import urlencode

from flask import Blueprint, request, redirect, abort, jsonify


from api import config


logger = logging.getLogger('flaskapp.blueprints.oauth')
bp = Blueprint('oauth', __name__)


@bp.route('/authorize', methods=['GET', 'POST'])
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

    return redirect(redirect_url)


@bp.route('/oauth_callback', methods=['GET', 'POST'])
def oauth_callback():
    logger.debug(request.get_data())
    logger.debug(request.args.to_dict())

    authorization_code = request.args.get('code')

    if authorization_code is None:
        logger.debug('unable to get "code" from callback')
        return abort(400)

    logger.debug('code: {}'.format(authorization_code))

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

    return jsonify(response)

