import logging

from flask import Blueprint
from flask import request

from api import helper

logger = logging.getLogger('flaskapp.blueprints.domains')
bp = Blueprint('domains', __name__)


@bp.route('/', methods=(['GET']))
def get_all():
    logger.debug('called domain:get_all')
    return helper.create_success_response([])

