# -*- coding: utf-8 -*-

import functools
import logger


def json_or_default(default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)

            if 200 <= r.status_code < 300:
                try:
                    return r.json()
                except Exception as exc:
                    logger.log('response json error: {exc}'.format(exc=exc))
            logger.log('response error: {resp}'.format(resp=r.text))
            return default
        return wrapper
    return decorator


def expect_status_code(*status_codes):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            r = func(*args, **kwargs)

            return r and r.status_code in status_codes
        return wrapper
    return decorator
