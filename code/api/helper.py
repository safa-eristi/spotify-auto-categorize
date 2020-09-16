# -*- coding: utf-8 -*-

from flask import jsonify


def create_response(is_success, message, payload, code=200):
    message = {
        'success': is_success,
        'message': message,
        'data': payload
    }
    response = jsonify(message)
    response.status_code = code
    return response


def create_success_response(message, payload, code=200):
    return create_response(True, message, payload, code)


def create_success_response(payload, code=200):
    return create_response(True, '', payload, code)


def create_error_response(message, code=200):
    return create_response(False, message, {}, code)


