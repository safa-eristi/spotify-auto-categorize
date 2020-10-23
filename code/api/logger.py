# -*- coding: utf-8 -*-

import codecs
import datetime
import logging
import sys


TS = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
LOGS_FOLDER = 'logs'
LOG_FILE_NAME = 'logs/{ts}.log'.format(ts=TS)

applog = logging.getLogger(__name__)
level_name = 'DEBUG'
level = logging.getLevelName(level_name)
formatter = logging.Formatter(
    '%(asctime)s | '
    '%(process)d | '
    '%(levelname)s | '
    '%(pathname)s | '
    '%(funcName)s | '
    '%(lineno)d | '
    '%(message)s'
)

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(level)
stream_handler.setFormatter(formatter)

applog.addHandler(stream_handler)

applog.setLevel(level)


def log(text):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log_text = '[{ts}] {text}'.format(ts=ts, text=text)

    print(log_text)
