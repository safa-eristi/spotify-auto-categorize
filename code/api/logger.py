# -*- coding: utf-8 -*-

import codecs
import datetime
import os

import config.settings


TS = datetime.datetime.utcnow().strftime('%Y%m%d%H%M%S')
LOGS_FOLDER = 'logs'
LOG_FILE_NAME = 'logs/{ts}.log'.format(ts=TS)


def log(text):
    ts = datetime.datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    log_text = '[{ts}] {text}'.format(ts=ts, text=text)

    print(log_text)
    
    if config.settings.LOG_TO_FILE:
        if not os.path.exists(LOGS_FOLDER):
            os.mkdir(LOGS_FOLDER)

        with codecs.open(LOG_FILE_NAME, 'a', 'utf-8') as f:
            f.write(log_text)
            f.write('\n')



